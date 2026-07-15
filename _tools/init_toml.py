import sys
import re
from pathlib import Path
from typing import Iterable, TextIO, TypeVar
from collections.abc import Callable, MutableMapping

import demjson3

from dfs_toml import DFSTomlEncoder
from markdown_converter import MarkdownBBCodeConverter as Converter

TEMPLATE_USAGE = "{} JSON_DIR INPUT_FILES..."

YOMI_VERSION = "1.9.20"
CONVERT_KEYS = ["signals", "constants", "properties", "methods"]
TYPED_KEYS = ["constants", "properties", "methods"]

T = TypeVar("T")

File_Path = Path(__file__).absolute()
Repo_Directory = File_Path.parent.parent

Classes_Directory = Repo_Directory / "docs/"


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


def convert_arr_to_dict(arr):
    return {
        item["name"]: {k: v for k, v in item.items() if k != "name"} for item in arr
    }


def convert_params(params: list[str]):
    new_params: dict[str, dict] = dict()
    for index, param in enumerate(params):
        param_name = param
        param_type = "UNKNOWN_TYPE"
        param_value = ""

        type_index = param.find(":")
        value_index = param.find("=")
        name_end = len(param)
        if type_index == -1:
            if value_index != -1:
                name_end = value_index
        else:
            name_end = type_index

        param_name = param[0:name_end]
        current_index = name_end + 1

        if type_index != -1:
            type_end = len(param) if value_index == -1 else value_index
            param_type = param[current_index:type_end]
            current_index = type_end + 1

        param_value = param[current_index:]

        # Replace UNKNOWN_TYPE to Variant
        if param_type == "UNKNOWN_TYPE":
            param_type = "Variant"

        new_params[param_name] = {
            "type": param_type,
            "value": param_value,
            "desc": "",
            "order": index,
        }

    return new_params


def load_old(fd: TextIO) -> dict:
    content = fd.read()

    match = re.search(r"let\s+data\s*=\s*(\{.*?\});", content, re.DOTALL)
    if not match:
        raise ValueError("Could not find the 'let data = ...' block inside the file.")

    js_object_string = match.group(1)
    return demjson3.decode(js_object_string)


def build_toml(input: Path, output: Path, encoder: DFSTomlEncoder):
    with open(input, "r") as fd:
        data = load_old(fd)

    # Reformat param values
    for key in data:
        is_typed_key = key in TYPED_KEYS
        for item in data[key]:
            if isinstance(item, dict):
                if item.get("type") == "UNKNOWN_TYPE":
                    item["type"] = "Variant"
                elif is_typed_key and "type" not in item:
                    item["type"] = "void"

            if "params" not in item:
                continue

            if not item["params"]:
                del item["params"]
                continue

            item["params"] = convert_params(item["params"])

        if key in CONVERT_KEYS and isinstance(data[key], list):
            data[key] = convert_arr_to_dict(data[key])

    converter = Converter()
    recursive_remap(data, "desc", converter.convert)

    data["version"] = YOMI_VERSION
    data["category"] = ""

    with open(output, "w") as fd:
        fd.write(encoder.dumps(data))


def build_dir(dir: Path, paths: Iterable[str], encoder: DFSTomlEncoder):
    Classes_Directory.mkdir(exist_ok=True)

    built_files: set[Path] = set()
    for path_str in paths:
        file = Path(path_str).absolute()
        if file in built_files:
            continue

        if not file.suffix.endswith("md"):
            print(f"Skipping {str(file.relative_to(Repo_Directory))}")
            continue

        output_path = Classes_Directory / file.relative_to(json_dir).with_suffix(
            ".toml"
        )
        try:
            build_toml(file, output_path, encoder)
        except ValueError:
            print(
                f"Failed to parse {str(file.relative_to(Repo_Directory))}! Skipping..."
            )
            continue

        built_files.add(file)

        print(
            f"{str(file.relative_to(Repo_Directory))} ->"
            f" {str(output_path.relative_to(Repo_Directory))}"
        )


if __name__ == "__main__":
    encoder = DFSTomlEncoder()

    if len(sys.argv) < 2:
        print(f"ERROR: Expected 2 or more args got {len(sys.argv) - 1}!")
        print(TEMPLATE_USAGE.format(sys.argv[0]))
        exit(1)

    json_dir = Path(sys.argv[1]).absolute()
    if not json_dir.is_dir():
        print("ERROR: Expected a valid dir for json_dir!")
        print(TEMPLATE_USAGE.format(sys.argv[0]))
        exit(1)

    build_dir(json_dir, sys.argv[2:], encoder)
