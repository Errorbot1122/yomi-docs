"""BBCode to RST

Architecture by Errorbot1122, Code by Gemini & Errorbot1122
"""

import re
from typing import Any, Optional

from converter import Parser, Handler, Converter


def _parse_params(raw_params: str) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if not raw_params or raw_params == "":
        return params

    raw_params = raw_params.strip()

    # [tag=value]
    if raw_params.startswith("="):
        params["default"] = raw_params[1:].strip("'\"")
        return params

    # [tag arg="val"]
    for k, v in re.findall(r'([\w_]+)\s*=\s*"([^"]*)"', raw_params):
        params[k] = v
    for k, v in re.findall(r"([\w_]+)\s*=\s*'([^']*)'", raw_params):
        params[k] = v

    # Standalone flags
    remaining = raw_params
    remaining = re.sub(r'[\w_]+\s*=\s*"[^"]*"', "", remaining)
    remaining = re.sub(r"[\w_]+\s*=\s*'[^']*'", "", remaining)
    remaining = re.sub(r'[\w_]+\s*=\s*[^\s"\']+', "", remaining)

    for flag in re.findall(r"([\w_]+)", remaining):
        params[flag] = True

    return params


# -- Parser Factories --
class TagParser(Parser):
    def __init__(self, tagname: str) -> None:
        self.tagname: str = tagname
        self._pattern: re.Pattern = re.compile(
            rf"\[{self.tagname}(?=[=\s\]])([^\]]*)\](.*?)\[/{self.tagname}\]", re.DOTALL
        )

    def parse(self, text: str) -> Optional[tuple[int, int, str, dict[str, Any]]]:
        match = self._pattern.search(text)
        if not match:
            return None

        raw_params, inner = match.groups()
        return match.start(), match.end(), inner, _parse_params(raw_params)


class VoidParser(Parser):
    def __init__(self, tagname: str) -> None:
        self.tagname: str = tagname
        # Added the same (?=[=\s\]]) lookahead constraint here
        self._pattern: re.Pattern = re.compile(
            rf"\[{self.tagname}(?=[=\s\]])([^\]]*)\]", re.DOTALL
        )

    def parse(self, text: str) -> Optional[tuple[int, int, dict[str, Any]]]:
        match = self._pattern.search(text)
        if not match:
            return None

        raw_params = match.group(1)
        return match.start(), match.end(), _parse_params(raw_params)


# -- Handler Factories --
class VoidSubstitutionHandler(Handler):
    """Generic layout handler for self-closing tags requiring a static string placement."""

    def __init__(self, replacement: str) -> None:
        self.replacement = replacement

    def handle(
        self, text: str, start_idx: int, end_idx: int, params: dict[str, Any]
    ) -> str:
        return self._slice_replace(text, start_idx, end_idx, self.replacement)


class EnclosingHandler(Handler):
    """Generic layout handler wrapping targeted inner boundaries with static prefixes/suffixes."""

    def __init__(self, prefix: str, suffix: str) -> None:
        self.prefix = prefix
        self.suffix = suffix

    def handle(
        self,
        text: str,
        start_idx: int,
        end_idx: int,
        inner: str,
        params: dict[str, Any],
    ) -> str:
        return self._slice_replace(
            text, start_idx, end_idx, f"{self.prefix}{inner}{self.suffix}"
        )


class ParagraphHandler(Handler):
    def handle(
        self,
        text: str,
        start_idx: int,
        end_idx: int,
        inner: str,
        params: dict[str, Any],
    ) -> str:
        align = params.get("align", params.get("default", "")).lower()
        if align in ["left", "center", "right", "fill"]:
            replacement = f"\n\n.. class:: {align}\n\n    {inner}\n\n"
        elif align in ["l", "c", "r", "f"]:
            class_map = {"l": "left", "c": "center", "r": "right", "f": "fill"}
            replacement = f"\n\n.. class:: {class_map[align]}\n\n    {inner}\n\n"
        else:
            replacement = f"\n\n{inner}\n\n"
        return self._slice_replace(text, start_idx, end_idx, replacement)


class URLHandler(Handler):
    def handle(
        self,
        text: str,
        start_idx: int,
        end_idx: int,
        inner: str,
        params: dict[str, Any],
    ) -> str:
        link = params.get("default", inner).strip()
        if link == inner:
            replacement = f"`{link} <{link}>`_"
        else:
            replacement = f"`{inner} <{link}>`_"
        return self._slice_replace(text, start_idx, end_idx, replacement)


class ImageHandler(Handler):
    def handle(
        self,
        text: str,
        start_idx: int,
        end_idx: int,
        inner: str,
        params: dict[str, Any],
    ) -> str:
        path = inner.strip()
        options = []
        if "width" in params:
            options.append(f"   :width: {params['width']}px")
        if "height" in params:
            options.append(f"   :height: {params['height']}px")

        opt_str = "\n" + "\n".join(options) if options else ""
        replacement = f"\n\n.. image:: {path}{opt_str}\n\n"
        return self._slice_replace(text, start_idx, end_idx, replacement)


class CharHandler(Handler):
    def handle(
        self, text: str, start_idx: int, end_idx: int, params: dict[str, Any]
    ) -> str:
        codepoint = params.get("default", "")
        if not codepoint:
            return self._slice_replace(text, start_idx, end_idx, "")
        try:
            char_val = chr(int(codepoint, 16))
            return self._slice_replace(text, start_idx, end_idx, char_val)
        except ValueError as e:
            print(e)
            return self._slice_replace(text, start_idx, end_idx, "")


# TODO: Make [br] add newline to list item
class ListHandler(Handler):
    def __init__(self, ordered: bool = False) -> None:
        self.ordered = ordered

    def handle(
        self,
        text: str,
        start_idx: int,
        end_idx: int,
        inner: str,
        params: dict[str, Any],
    ) -> str:
        lines = [line.strip() for line in inner.strip().splitlines() if line.strip()]
        prefix = "1. " if self.ordered else "* "
        formatted_items = "\n".join(f"{prefix}{line}" for line in lines)
        replacement = f"\n\n{formatted_items}\n\n"
        return self._slice_replace(text, start_idx, end_idx, replacement)


class TableHandler(Handler):
    def handle(
        self,
        text: str,
        start_idx: int,
        end_idx: int,
        inner: str,
        params: dict[str, Any],
    ) -> str:
        cols = params.get("default", "1")
        cells = re.findall(r"\[cell.*?\](.*?)\[/cell\]", inner, re.DOTALL)
        if not cells:
            return self._slice_replace(text, start_idx, end_idx, "")

        try:
            col_count = int(cols)
        except ValueError:
            col_count = 1

        output = ["\n\n.. list-table::\n   :widths: " + " ".join(["10"] * col_count)]
        for i, cell in enumerate(cells):
            item_prefix = "   * - " if i % col_count == 0 else "     - "
            output.append(f"{item_prefix}{cell.strip()}")

        replacement = "\n".join(output) + "\n\n"
        return self._slice_replace(text, start_idx, end_idx, replacement)


class CodeBlockHandler(Handler):
    def handle(
        self,
        text: str,
        start_idx: int,
        end_idx: int,
        inner: str,
        params: dict[str, Any],
    ) -> str:
        # If there are no parameters, process as a standard inline literal code segment
        if not params:
            return self._slice_replace(text, start_idx, end_idx, f"``{inner}``")

        # Resolve the language tag identifier (supporting both default syntax [code=lang] and [code lang="lang"])
        lang = params.get("lang", params.get("default", ""))

        # Build the RST code-block header directive
        lines = [f".. code-block:: {lang}"]

        # Process any additional tag options as sphinx directive arguments
        for k, v in params.items():
            if k in ("lang", "default"):
                continue
            # If the option parameter is a boolean flag
            if v is True:
                lines.append(f"   :{k}:")
            else:
                lines.append(f"   :{k}: {v}")

        # Add empty padding spacer line before inner body indentation
        lines.append("")

        # Indent code body to conform to RST directive block rules
        indented_code = "\n".join(f"    {line}" for line in inner.splitlines())
        lines.append(indented_code)

        # Build padded substitution block to avoid adjacent markup merging errors
        replacement = f"\n\n" + "\n".join(lines) + f"\n\n"
        return self._slice_replace(text, start_idx, end_idx, replacement)


# -- Tag Registration API --
# TODO: Ignore bbcode inside tags
class BBCodeRSTConverter(Converter):
    def __init__(self) -> None:
        super().__init__()

        self.add_shield(
            TagParser("code"),
            shield_order=-1,
            unshield_order=98,
            unshield_handler=CodeBlockHandler(),
        )

        self.add_rst_tag("b", "**")
        self.add_rst_tag("i", "*")
        self.add_rst_tag("u", ":underline:`", "`")
        self.add_rst_tag("s", ":strike:`", "`")

        self.add_tag(TagParser("p"), ParagraphHandler())

        # FIXME: Handle multi-lines
        self.add_tag(TagParser("indent"), EnclosingHandler("\n\n   ", "\n\n"))
        self.add_tag(
            TagParser("center"),
            EnclosingHandler("\n\n.. class:: center\n\n    ", "\n\n"),
        )
        self.add_tag(
            TagParser("left"), EnclosingHandler("\n\n.. class:: left\n\n    ", "\n\n")
        )
        self.add_tag(
            TagParser("right"), EnclosingHandler("\n\n.. class:: right\n\n   ", "\n\n")
        )
        self.add_tag(
            TagParser("fill"), EnclosingHandler("\n\n.. class:: fill\n\n   ", "\n\n")
        )

        self.add_rst_tag("br", "\n", is_void=True)
        self.add_rst_tag("hr", "\n\n----\n\n", is_void=True)

        self.add_tag(TagParser("url"), URLHandler())
        self.add_tag(TagParser("img"), ImageHandler())
        self.add_tag(VoidParser("char"), CharHandler())

        self.add_tag(TagParser("table"), TableHandler())
        self.add_tag(TagParser("ul"), ListHandler(ordered=False))
        self.add_tag(TagParser("ol"), ListHandler(ordered=True))

        self.add_tag(TagParser("cell"), EnclosingHandler("", ""), order=11)

        unicode_controls = {
            "lrm": "\u200e",
            "rlm": "\u200f",
            "lre": "\u202a",
            "rle": "\u202b",
            "lro": "\u202d",
            "rlo": "\u202e",
            "pdf": "\u202c",
            "alm": "\u061c",
            "lri": "\u2066",
            "rli": "\u2067",
            "fsi": "\u2068",
            "pdi": "\u2069",
            "zwj": "\u200d",
            "zwnj": "\u200c",
            "wj": "\u2060",
            "shy": "\u00ad",
        }
        for tag, char_val in unicode_controls.items():
            self.add_tag(VoidParser(tag), VoidSubstitutionHandler(char_val), order=98)

        self.add_tag(VoidParser("lb"), VoidSubstitutionHandler("["), order=99)
        self.add_tag(VoidParser("rb"), VoidSubstitutionHandler("]"), order=99)

    def add_tag(self, parser: Parser, handler: Handler, order: int = 10):
        """Forwards registration parameters to the engine's ordered pipeline layer."""
        self.add_convert(parser, handler, order=order)

    def add_rst_tag(
        self,
        tagname: str,
        prefix: str,
        suffix: Optional[str] = None,
        is_void: bool = False,
        order: int = 10,
    ):
        if is_void:
            self.add_tag(
                VoidParser(tagname), VoidSubstitutionHandler(prefix), order=order
            )
            return

        self.add_tag(
            TagParser(tagname), EnclosingHandler(prefix, suffix or prefix), order=order
        )


if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 2, f"INCORRECT ARG COUNT! Expected 2 got {len(sys.argv)}!"

    converter = BBCodeRSTConverter()
    print(converter.convert(sys.argv[1]))
