import sys
import re
import json
from typing import Literal, Optional, TypedDict, Any, cast, overload
from collections.abc import Callable, MutableMapping, Mapping
from itertools import zip_longest
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from tomllib import load

from converter import Parser, Handler
from bbcode_converter import (
    BBCodeRSTConverter as Converter,
    TagParser,
    EnclosingHandler,
)

USAGE_STRING = "'{}' class_src_dir|-s|--skip-warning"

NO_DESC_TEXT = "No description provided."


File_Path = Path(__file__).absolute()
Repo_Directory = File_Path.parent.parent

Output_Directory = Repo_Directory / "class_ref/"
Template_Directory = Repo_Directory / "_templates/"
Source_Directory = Repo_Directory / "classes/"

Types_Directory = Repo_Directory / "types/"
Index_Path = Output_Directory / "index.rst"
Builtins_JSON_Path = Repo_Directory / "_static/godot-classes.json"


def escape_rst(text: Any) -> str:
    if text is None:
        return ""

    s = str(text)
    special_chars = r"\*`[]|_"
    escaped = []
    for char in s:
        if char in special_chars:
            escaped.append("\\" + char)
        else:
            escaped.append(char)
    return "".join(escaped)


Template_Env = Environment(loader=FileSystemLoader(Template_Directory))
Template_Env.filters["escape_rst"] = escape_rst
Build_Template = Template_Env.get_template("class.rst.j2")
Index_Template = Template_Env.get_template("index.rst.j2")

type Data = dict[str, Any]


class ItemData(TypedDict):
    # Custom sphinx reference name to use
    _ref: Optional[str]

    # Description for the item
    desc: Optional[str]


class ParamData(TypedDict):
    type: Optional[str]
    value: Optional[str]
    _order: Optional[int]


class VariableData(ItemData):
    # The type designated type for the var
    type: str
    # The value stored in the var
    value: Optional[str]


class ConstantData(ItemData):
    # The value stored in the constant
    value: str


class PropertyData(VariableData):
    # Flag for if the property is exported
    export: Optional[bool]
    # Flag for if the property is defined right as the _ready() signal is
    # called
    onready: Optional[bool]


class FunctionLikeData(ItemData):
    # Input arguments for the function
    params: Optional[dict[str, ParamData]]


SignalData = FunctionLikeData


class MethodData(FunctionLikeData):
    # The return type of the callable
    type: Optional[str]


# TODO: Add short desc later
class ClassData(ItemData):
    # YOMI Version
    version: str
    # Last updated
    updated: str
    # Class's Name
    name: Optional[str]
    # Sidebar Category field
    category: str
    # The class name it extends
    inherits: Optional[str]
    # The Godot path for where the script class's script is stored
    script_path: str
    # The main scene the class debuts in
    scene_path: Optional[str]

    signals: Optional[dict[str, SignalData]]
    constants: Optional[dict[str, ConstantData]]
    properties: Optional[dict[str, PropertyData]]
    methods: Optional[dict[str, MethodData]]


class BuildClassData(ClassData):
    ref_name: str


class ArgsData(TypedDict):
    source_dir: Path


def get_ref_uri(class_name: str, item_type: str = "", item_name: str = "") -> str:
    if not item_type or item_type.lower() == "class" or not item_name:
        return f"class_{class_name}".lower()

    type_to_role = {
        "member": "property",
        "prop": "property",
        "property": "property",
        "meth": "method",
        "method": "method",
        "const": "constant",
        "constant": "constant",
        "sig": "signal",
        "signal": "signal",
    }

    role = type_to_role.get(item_type.lower(), "property")
    return f"class_{class_name}_{role}_{item_name}".lower()


def render_ref(ref: str, display: Optional[str] = None) -> str:
    if not display:
        return f":ref:`{ref}`"
    else:
        return f":ref:`{display}<{ref}>`"


class ReferenceLinkParser(Parser):
    def __init__(
        self,
        current_class: str,
        current_item: str = "",
        current_item_type: str = "class",
    ) -> None:
        self.current_class = current_class
        self.current_item = current_item
        self.current_item_type = current_item_type

        self._pattern: re.Pattern = re.compile(r"\[\[(.*?)\]\]", re.DOTALL)

    def parse(
        self, text: str
    ) -> Optional[tuple[int, int, str | None, str | None, str | None, str, str, str]]:
        match = self._pattern.search(text)
        if not match:
            return None

        content = match.group(1).strip()
        link_type = None
        target = None
        custom_display = None

        if "|" in content:
            main_content, custom_display = content.split("|", 1)
            main_content = main_content.strip()
            custom_display = custom_display.strip()
        else:
            main_content = content

        if main_content:
            parts = main_content.split(maxsplit=1)
            link_type = parts[0]
            if len(parts) > 1:
                target = parts[1]

        return (
            match.start(),
            match.end(),
            link_type,
            target,
            custom_display,
            self.current_class,
            self.current_item,
            self.current_item_type,
        )


class ReferenceLinkHandler(Handler):
    def handle(
        self,
        text: str,
        start_idx: int,
        end_idx: int,
        link_type: str | None,
        target: str | None,
        custom_display: str | None,
        current_class: str,
        current_item: str,
        current_item_type: str,
    ) -> str:
        if link_type == "ref":
            target_anchor = target.lower() if target else ""
            if custom_display is not None:
                replacement = " " + render_ref(target_anchor, custom_display) + " "
            else:
                display_text = target if target else ""
                replacement = " " + render_ref(target_anchor, "^" + display_text) + " "
            return self._slice_replace(text, start_idx, end_idx, replacement)

        is_autodetect = (link_type == "prop" or link_type is None) and target is None

        resolved_type = "autodetect" if is_autodetect else (link_type or "autodetect")
        resolved_class = current_class
        resolved_item = ""

        if not is_autodetect:
            if target:
                if "." in target:
                    resolved_class, resolved_item = target.split(".", 1)
                else:
                    if link_type == "class":
                        resolved_class = target
                    else:
                        resolved_class = current_class
                        resolved_item = target
            else:
                if link_type == "class":
                    resolved_class = current_class

        type_to_role = {
            "class": "class",
            "member": "property",
            "prop": "property",
            "meth": "method",
            "method": "method",
            "const": "constant",
            "constant": "constant",
            "sig": "signal",
            "signal": "signal",
        }
        if resolved_type == "autodetect":
            resolved_item = resolved_item or current_item
            resolved_role = type_to_role.get(current_item_type.lower(), "property")
        else:
            resolved_role = type_to_role.get(resolved_type, "property")

        target_anchor = get_ref_uri(resolved_class, resolved_role, resolved_item)
        if custom_display is not None:
            replacement = " " + render_ref(target_anchor, custom_display) + " "
        else:
            if resolved_role == "class":
                display_text = resolved_class
            else:
                if resolved_class == current_class:
                    display_text = resolved_item
                else:
                    display_text = f"{resolved_class}.{resolved_item}"

                if resolved_role in ["method", "signal"]:
                    display_text = display_text + "()"

            replacement = " " + render_ref(target_anchor, "^" + display_text) + " "

        return self._slice_replace(text, start_idx, end_idx, replacement)


class EngineHandler(Handler):
    """Deletes the tag and all of its inner content from the output."""

    def handle(
        self,
        text: str,
        start_idx: int,
        end_idx: int,
        inner: str,
        params: dict[str, Any],
    ) -> str:
        return self._slice_replace(text, start_idx, end_idx, "")


@overload
def better_get[T, K](obj: Mapping[str, T], key: str, default: K) -> T | K: ...
@overload
def better_get[T, K](
    obj: Mapping[str, T], key: str, default: None = None
) -> T | None: ...
def better_get[T, K](
    obj: Mapping[str, T], key: str, default: Optional[K] = None
) -> T | K | None:
    assert isinstance(obj, Mapping)
    return obj.get(key, default) or default


def recursive_remap[T](
    obj: object,
    key: str,
    modifier: Callable[[T], T],
) -> None:
    if isinstance(obj, MutableMapping):
        for k, v in obj.items():
            if k == key:
                obj[k] = modifier(v)

            if isinstance(v, (MutableMapping, list)):
                recursive_remap(v, key, modifier)

    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (MutableMapping, list)):
                recursive_remap(item, key, modifier)


def parse_args(argv=()) -> ArgsData:
    source_dir = Source_Directory
    if len(argv) != 2:
        print(
            "WARNING: Must have at exactly 1 argument! Usage: "
            + USAGE_STRING.format(argv[0])
        )
        print(
            "         Defaulting to"
            f" '{str(Source_Directory.relative_to(Repo_Directory, walk_up=True))}'"
        )
    elif not (argv[1].lower() == "-s" or argv[1].lower() == "--skip-warning"):
        source_dir = Path(argv[1]).absolute()

    assert source_dir.exists(), (
        "Source directory"
        f" '{str(source_dir.relative_to(Repo_Directory, walk_up=True))}' dose not"
        " exists!"
    )
    return ArgsData({"source_dir": source_dir})


def read_class_data(file: Path) -> ClassData:
    with open(file, "rb") as fd:
        return cast(ClassData, load(fd))


def _get_property_priority(item_tuple) -> int:
    _, data = item_tuple

    is_export = data.get("export", False)
    is_onready = data.get("onready", False)

    if is_export and is_onready:
        return 0
    if is_export:
        return 1
    if is_onready:
        return 2
    return 3


def _sort_functions[T: FunctionLikeData](functions: dict[str, T]) -> dict[str, T]:
    def _sort_parameters(params: dict[str, Any]) -> dict[str, Any]:
        if not params:
            return params

        ordered_items: list[tuple[str, Any, int]] = []
        unordered_items: list[tuple[str, Any]] = []

        for name, data in params.items():
            order = data.get("_order") if isinstance(data, dict) else None
            if order is not None:
                try:
                    ordered_items.append((name, data, int(order)))
                except (ValueError, TypeError):
                    unordered_items.append((name, data))
            else:
                unordered_items.append((name, data))

        ordered_items.sort(key=lambda x: x[2])

        max_order = max((item[2] for item in ordered_items), default=-1)
        allocated_size = max(max_order + 1, len(params))
        slots: list[Optional[tuple[str, Any]]] = [None] * allocated_size

        for name, data, order in ordered_items:
            target_idx = order
            while target_idx < len(slots) and slots[target_idx] is not None:
                target_idx += 1

            if target_idx >= len(slots):
                slots.extend([None] * (target_idx - len(slots) + 1))

            slots[target_idx] = (name, data)

        unordered_iter = iter(unordered_items)
        for i in range(len(slots)):
            if slots[i] is None:
                try:
                    slots[i] = next(unordered_iter)
                except StopIteration:
                    break

        for item in unordered_iter:
            slots.append(item)

        return {
            name: data for slot in slots if slot is not None for name, data in [slot]
        }

    sorted_functions: dict[str, T] = {}
    for func_name in sorted(functions.keys(), key=lambda x: x.lower()):
        func_data = cast(T, dict(functions[func_name]))

        if "params" in func_data and isinstance(func_data["params"], dict):
            func_data["params"] = _sort_parameters(func_data["params"])

        sorted_functions[func_name] = func_data

    return sorted_functions  # Handle main description and refs


# TODO: Add Path as field, and use ref_name as key
def _set_valid_names(
    classes: dict[Path, ClassData],
) -> dict[Path, BuildClassData]:
    file_paths_list = list(classes.keys())
    classes_list = [classes[path] for path in file_paths_list]
    all_class_segments = []

    for class_data in classes_list:
        explicit_name = class_data.get("name")
        if explicit_name:
            segments = [explicit_name]
        else:
            raw_path = class_data.get("script_path", "")
            clean_path = raw_path.replace("res://", "")
            raw_segments = [seg for seg in clean_path.split("/") if seg]

            segments = []
            for seg in raw_segments:
                if seg.endswith(".gd") or seg.endswith(".cs"):
                    segments.append(seg[:-3])
                else:
                    segments.append(seg)
        all_class_segments.append(segments)

    reversed_segments_list = [list(reversed(seg)) for seg in all_class_segments]
    total_classes = len(classes_list)
    required_depths = [1] * total_classes

    for i in range(total_classes):
        for j in range(total_classes):
            if i == j:
                continue

            difference_index = -1
            for idx, (seg_a, seg_b) in enumerate(
                zip_longest(reversed_segments_list[i], reversed_segments_list[j])
            ):
                if seg_a != seg_b:
                    difference_index = idx
                    break

            if difference_index == -1:
                raise ValueError(
                    "Collision unresolved because path segments are completely"
                    f" identical: {classes_list[i].get('script_path')} and"
                    f" {classes_list[j].get('script_path')}"
                )

            required_depths[i] = max(required_depths[i], difference_index + 1)

    resolved_names = []
    for i in range(total_classes):
        segments = reversed_segments_list[i]
        depth = min(required_depths[i], len(segments))
        chosen_segments = reversed(segments[:depth])
        resolved_names.append("/".join(chosen_segments))

    resolved_classes = {}
    for i in range(total_classes):
        path = file_paths_list[i]
        class_data = classes_list[i]

        build_data = cast(BuildClassData, dict(class_data))
        build_data["ref_name"] = resolved_names[i]
        resolved_classes[path] = build_data

    return resolved_classes


def _sanitize_class_path(name: str) -> str:
    return name.lower().replace("/", "_")


# TODO: Handle signal/method param desc
def build_class(
    path: Path,
    class_data: BuildClassData,
    all_classes: dict[Path, BuildClassData] = {},
    builtins: dict[str, list[str]] = {},
):
    data: BuildClassData = class_data.copy()

    def _convert_desc(
        text: str, current_item: str = "", current_item_type: str = "class"
    ) -> str:
        converter = Converter()
        converter.add_shield(
            TagParser("raw"),
            shield_order=-2,
            unshield_order=100,
            unshield_handler=EnclosingHandler("", ""),
        )
        converter.add_tag(TagParser("external"), EngineHandler(), order=0)
        converter.add_tag(TagParser("docs"), EnclosingHandler("", ""), order=1)

        converter.add_tag(
            ReferenceLinkParser(data["ref_name"], current_item, current_item_type),
            ReferenceLinkHandler(),
            order=2,
        )

        return converter.convert(text)

    def _get_ancestors_line() -> str:
        SEPARATOR = " **<** "

        # FIXME: Could cause slowdown as it re-generates for each class
        name_map = {x["ref_name"]: x for x in all_classes.values()}
        path_map = {x["script_path"]: x for x in all_classes.values()}

        ancestor_refs: list[str] = []
        current_data: Optional[BuildClassData] = data
        current_parent = cast(str, better_get(data, "inherits", ""))
        while current_parent:

            class_name: str = ""
            if current_parent.lower() in builtins:
                ancestor_refs.append(render_ref(get_ref_uri(current_parent.lower())))
                ancestor_refs += [
                    render_ref(get_ref_uri(x)) for x in builtins[current_parent.lower()]
                ]
                break
            elif current_parent in name_map:
                current_data = name_map[current_parent]
                class_name = current_parent
            elif current_parent in path_map:
                current_data = path_map[current_parent]
                class_name = current_data["ref_name"]
            else:
                break

            ancestor_refs.append(render_ref(get_ref_uri(class_name)))
            current_parent = cast(str, better_get(current_data, "inherits", ""))

        return SEPARATOR.join(ancestor_refs)

    def _get_children_line() -> str:
        children_refs: list[str] = []
        for current_class in all_classes.values():
            parent = current_class.get("inherits")

            if not (parent == data["ref_name"] or parent == data["script_path"]):
                continue

            children_refs.append(render_ref(get_ref_uri(current_class["ref_name"])))
        return ", ".join(sorted(children_refs))

    def _handle_func(key: Literal["method"] | Literal["signal"]):
        funcs = data.get(key + "s")
        if funcs is None:
            return

        for name, func in funcs.items():
            func["desc"] = _convert_desc(
                better_get(cast(Data, func), "desc", NO_DESC_TEXT), name, key
            )
            if not func.get("type"):
                func["type"] = "unknown"

            for param_name, param in better_get(cast(Data, func), "params", {}).items():
                param["desc"] = _convert_desc(
                    better_get(cast(Data, param), "desc", NO_DESC_TEXT), name, key
                )
                if not param.get("type"):
                    param["type"] = "unknown"

            func["_ref"] = func.get(
                "_ref", get_ref_uri(class_data["ref_name"], key, name)
            )

        data[key + "s"] = cast(
            Any,
            _sort_functions(cast(dict[str, FunctionLikeData], data[key + "s"])),
        )

    data["desc"] = _convert_desc(better_get(cast(Data, data), "desc", NO_DESC_TEXT))
    data["_ref"] = data.get("_ref", get_ref_uri(data["ref_name"]))

    # Sort keys
    # FIXME: Escape name chars with backslash
    if "properties" in data and data["properties"] is not None:
        for prop_name, prop in data["properties"].items():
            # Handle property description and refs
            prop["desc"] = _convert_desc(
                better_get(cast(Data, prop), "desc", NO_DESC_TEXT), prop_name, "prop"
            )

            # Add null to all props
            if not prop.get("value"):
                prop["value"] = "null"

            if not prop.get("type"):
                prop["type"] = "unknown"

            prop["_ref"] = prop.get(
                "_ref", get_ref_uri(data["ref_name"], "prop", prop_name)
            )

        sorted_properties = sorted(
            data["properties"].items(), key=lambda x: x[0].lower()
        )
        data["properties"] = dict(sorted(sorted_properties, key=_get_property_priority))

    if "constants" in data and data["constants"] is not None:
        # Handle consent description and refs
        for const_name, const in data["constants"].items():
            const["desc"] = _convert_desc(
                better_get(cast(Data, const), "desc", NO_DESC_TEXT), const_name, "const"
            )
            const["_ref"] = const.get(
                "_ref", get_ref_uri(data["ref_name"], "const", const_name)
            )

        data["constants"] = dict(
            sorted(data["constants"].items(), key=lambda x: x[0].lower())
        )

    if "methods" in data and data["methods"] is not None:
        _handle_func("method")

    if "signals" in data and data["signals"] is not None:
        _handle_func("signal")

    template_data = cast(dict[str, Any], data)
    template_data["ancestors"] = _get_ancestors_line()
    template_data["children"] = _get_children_line()

    # Build the class reference RST
    rendered = Build_Template.render(template_data)

    target_path = Output_Directory / f"{_sanitize_class_path(data["ref_name"])}.rst"
    with open(target_path, "w", encoding="utf-8") as fd:
        fd.write(rendered)

    print(
        f"{str(path.relative_to(Repo_Directory, walk_up=True))} ->"
        f" {str(target_path.relative_to(Repo_Directory, walk_up=True))}"
    )


def build_index(all_classes: dict[Path, BuildClassData]):
    categories: dict[str, list[str]] = {}
    for class_data in all_classes.values():
        category_name = class_data.get("category", "Uncategorized")
        if category_name not in categories:
            categories[category_name] = []

        categories[category_name].append(_sanitize_class_path(class_data["ref_name"]))

    sorted_categories = {}
    for category in sorted(categories.keys()):
        sorted_categories[category] = sorted(categories[category])

    sorted_categories["Types"] = []
    for typed_path in sorted(Types_Directory.glob("*.rst")):
        sorted_categories["Types"].append(
            typed_path.relative_to(Output_Directory, walk_up=True)
        )

    rendered = Index_Template.render(categories=sorted_categories)
    with open(Index_Path, "w", encoding="utf-8") as fd:
        fd.write(rendered)

    print(
        "Index built at path: "
        + str(Index_Path.relative_to(Repo_Directory, walk_up=True))
    )


def build_dir(dir: Path):
    with open(Builtins_JSON_Path, "r") as fd:
        builtins: dict[str, list[str]] = json.load(fd)

    Output_Directory.mkdir(exist_ok=True)

    class_datas: dict[Path, ClassData] = {}
    for file in dir.glob("*.toml"):
        assert file.suffix.endswith(
            "toml"
        ), f"'{file.relative_to(Repo_Directory, walk_up=True)}' is not a '.toml'"

        try:
            class_datas[file] = read_class_data(file)
        except Exception as e:
            print(
                "ENCOUNTERED ERROR WHILST READING: ",
                file.relative_to(Repo_Directory, walk_up=True),
            )
            raise e

    all_classes = _set_valid_names(class_datas)
    for file_path, class_data in all_classes.items():
        try:
            build_class(file_path, class_data, all_classes, builtins)
        except Exception as e:
            print(
                f"ENCOUNTERED ERROR WHILST BUILDING: {class_data["ref_name"]} ("
                + str(file_path.relative_to(Repo_Directory, walk_up=True))
                + ")"
            )
            raise e

    try:
        build_index(all_classes)
    except Exception as e:
        print("ENCOUNTERED ERROR WHILST BUILDING INDEX FILE!")
        raise e


if __name__ == "__main__":
    Output_Directory.mkdir(exist_ok=True)

    source_dir = parse_args(sys.argv)["source_dir"]
    build_dir(source_dir)
