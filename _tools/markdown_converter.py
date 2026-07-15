"""Markdown to BBCode Converter

Architecture by Errorbot1122, Code by Gemini & Errorbot1122
"""

import re
import sys
from typing import Optional

from converter import Parser, Handler, Converter


# -- Custom Parser Factories --
class BlockCodeParser(Parser):
    """Parses multi-line markdown code blocks."""

    def __init__(self) -> None:
        # \x60{3} = Triple Backtick to avoid Canvas rendering issues
        self._pattern = re.compile(r"(?m)^\x60{3}(?:\w+)?\n([\s\S]*?)\n\x60{3}")

    def parse(self, text: str) -> Optional[tuple[int, int, str]]:
        match = self._pattern.search(text)
        if not match:
            return None
        return match.start(), match.end(), match.group(1)


class InlineCodeParser(Parser):
    """Parses single-line markdown inline code execution blocks supporting single or multiple backticks."""

    def __init__(self) -> None:
        self._pattern = re.compile(r"(`+)([^`\n]+)\1")

    def parse(self, text: str) -> Optional[tuple[int, int, str]]:
        match = self._pattern.search(text)
        if not match:
            return None
        return match.start(), match.end(), match.group(2)


class HeaderParser(Parser):
    """Parses structured markdown headers based on their prefix depth level."""

    def __init__(self, level: int) -> None:
        self.level = level
        self._pattern = re.compile(rf"(?m)^#{self.level}[ \t]+(.*)$")

    def parse(self, text: str) -> Optional[tuple[int, int, str]]:
        match = self._pattern.search(text)
        if not match:
            return None
        return match.start(), match.end(), match.group(1)


class ListBlockParser(Parser):
    """Parses continuous blocks of ordered or unordered markdown list items."""

    def __init__(self) -> None:
        self._pattern = re.compile(r"(?m)((?:^[ \t]*(?:\d+\.|[*+-])[ \t]+.+\n?)+)")

    def parse(self, text: str) -> Optional[tuple[int, int, str, bool]]:
        match = self._pattern.search(text)
        if not match:
            return None

        block = match.group(1)
        first_line = block.lstrip()
        is_ordered = bool(re.match(r"^\d+\.", first_line))

        return match.start(), match.end(), block, is_ordered


class LinkImageParser(Parser):
    """Parses explicit markdown media elements and hyperlinks."""

    def __init__(self, is_image: bool = False) -> None:
        self.is_image = is_image
        if is_image:
            self._pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
        else:
            self._pattern = re.compile(r"\[(.*?)\]\((.*?)\)")

    def parse(self, text: str) -> Optional[tuple[int, int, str, str]]:
        match = self._pattern.search(text)
        if not match:
            return None
        return match.start(), match.end(), match.group(1), match.group(2)


class InlineElementParser(Parser):
    """Parses inline typographic styles cleanly using balanced custom bounds."""

    def __init__(self, delimiters: list[str]) -> None:
        self._patterns = []
        for delim in delimiters:
            delim_esc = re.escape(delim)
            self._patterns.append(re.compile(rf"{delim_esc}(.+?){delim_esc}"))

    def parse(self, text: str) -> Optional[tuple[int, int, str]]:
        for pattern in self._patterns:
            match = pattern.search(text)
            if not match:
                continue
            return match.start(), match.end(), match.group(1)
        return None


class SpecialCharParser(Parser):
    """Finds unescaped special control characters and brackets to protect or translate."""

    def __init__(self) -> None:
        self.char_map = {
            "\u200e": "lrm",
            "\u200f": "rlm",
            "\u202a": "lre",
            "\u202b": "rle",
            "\u202d": "lro",
            "\u202e": "rlo",
            "\u202c": "pdf",
            "\u061c": "alm",
            "\u2066": "lri",
            "\u2067": "rli",
            "\u2068": "fsi",
            "\u2069": "pdi",
            "\u200d": "zwj",
            "\u200c": "zwnj",
            "\u2060": "wj",
            "\u00ad": "shy",
        }
        self._pattern = re.compile(
            r"[\u200e\u200f\u202a\u202b\u202d\u202e\u202c\u061c\u2066\u2067\u2068\u2069\u200d\u200c\u2060\u00ad\[\]]"
        )

    def parse(self, text: str) -> Optional[tuple[int, int, str]]:
        valid_tags = {
            "b",
            "/b",
            "i",
            "/i",
            "s",
            "/s",
            "code",
            "/code",
            "img",
            "/img",
            "url",
            "/url",
            "ul",
            "/ul",
            "ol",
            "/ol",
            "*",
            "lb",
            "rb",
            "lrm",
            "rlm",
            "lre",
            "rle",
            "lro",
            "rlo",
            "pdf",
            "alm",
            "lri",
            "rli",
            "fsi",
            "pdi",
            "zwj",
            "zwnj",
            "wj",
            "shy",
            "size",
            "/size",
        }

        for match in self._pattern.finditer(text):
            char = match.group(0)
            idx = match.start()

            if char in self.char_map:
                return idx, idx + 1, self.char_map[char]

            if char == "[":
                end_bracket = text.find("]", idx)
                if end_bracket != -1:
                    tag_content = text[idx + 1 : end_bracket]
                    tag_base = tag_content.split("=")[0].split(" ")[0]
                    if tag_base in valid_tags:
                        continue
                return idx, idx + 1, "lb"

            if char == "]":
                start_bracket = text.rfind("[", 0, idx)
                if start_bracket != -1:
                    tag_content = text[start_bracket + 1 : idx]
                    tag_base = tag_content.split("=")[0].split(" ")[0]
                    if tag_base in valid_tags:
                        continue
                return idx, idx + 1, "rb"

        return None


# -- Handler Factories --
class EnclosingHandler(Handler):
    """Generic layout handler wrapping targeted inner boundaries with static prefixes/suffixes."""

    def __init__(self, prefix: str, suffix: str) -> None:
        self.prefix = prefix
        self.suffix = suffix

    def handle(self, text: str, start_idx: int, end_idx: int, inner: str) -> str:
        return self._slice_replace(
            text, start_idx, end_idx, f"{self.prefix}{inner}{self.suffix}"
        )


class LinkHandler(Handler):
    """Handler for processing standard inline Markdown links into BBCode URL format."""

    def handle(
        self, text: str, start_idx: int, end_idx: int, link_text: str, url: str
    ) -> str:
        return self._slice_replace(
            text, start_idx, end_idx, f"[url={url.strip()}]{link_text}[/url]"
        )


class ImageHandler(Handler):
    """Handler for processing inline Markdown images into BBCode image tags."""

    def handle(
        self, text: str, start_idx: int, end_idx: int, alt_text: str, url: str
    ) -> str:
        return self._slice_replace(
            text, start_idx, end_idx, f"[img]{url.strip()}[/img]"
        )


class ListHandler(Handler):
    """Handler for transforming contiguous Markdown lists into nested itemized BBCode layouts."""

    def handle(
        self, text: str, start_idx: int, end_idx: int, block: str, ordered: bool
    ) -> str:
        lines = block.strip("\n").split("\n")
        bb_items = []

        for line in lines:
            if not line.strip():
                continue
            cleaned = line.strip()
            if ordered:
                cleaned = re.sub(r"^\d+\.[ \t]+", "", cleaned)
            else:
                cleaned = re.sub(r"^[*+-][ \t]+", "", cleaned)
            bb_items.append(f"[*] {cleaned}")

        list_tag = "ol" if ordered else "ul"
        replacement = (
            f"\n\n[{list_tag}]\n" + "\n".join(bb_items) + f"\n[/{list_tag}]\n\n"
        )
        return self._slice_replace(text, start_idx, end_idx, replacement)


class SpecialCharHandler(Handler):
    """Generates standard bracketed substitution structures for special characters."""

    def handle(self, text: str, start_idx: int, end_idx: int, tag_name: str) -> str:
        return self._slice_replace(text, start_idx, end_idx, f"[{tag_name}]")


# -- Tag Registration API --
class MarkdownBBCodeConverter(Converter):
    def __init__(self) -> None:
        super().__init__()

        self.add_shield(
            BlockCodeParser(),
            shield_order=-99,
            unshield_order=98,
            unshield_handler=EnclosingHandler("[code]\n", "\n[/code]"),
        )
        self.add_shield(
            InlineCodeParser(),
            shield_order=-99,
            unshield_order=98,
            unshield_handler=EnclosingHandler("[code]", "[/code]"),
        )

        self.add_shield(
            LinkImageParser(is_image=True),
            shield_order=-98,
            unshield_order=1,
            unshield_handler=ImageHandler(),
        )
        self.add_shield(
            LinkImageParser(is_image=False),
            shield_order=-98,
            unshield_order=1,
            unshield_handler=LinkHandler(),
        )

        self.add_tag(HeaderParser(1), EnclosingHandler("[b]", "[/b]"))
        self.add_tag(HeaderParser(2), EnclosingHandler("[b]", "[/b]"))
        self.add_tag(HeaderParser(3), EnclosingHandler("[b]", "[/b]"))

        self.add_tag(ListBlockParser(), ListHandler())

        self.add_tag(InlineElementParser(["**", "__"]), EnclosingHandler("[b]", "[/b]"))
        self.add_tag(InlineElementParser(["*", "_"]), EnclosingHandler("[i]", "[/i]"))
        self.add_tag(InlineElementParser(["~~"]), EnclosingHandler("[s]", "[/s]"))

        self.add_tag(SpecialCharParser(), SpecialCharHandler(), order=2)

    def add_tag(self, parser: Parser, handler: Handler, order: int = 0) -> None:
        """Forwards registration parameters to the engine's pipeline."""
        self.add_convert(parser, handler, order=order)


if __name__ == "__main__":
    assert len(sys.argv) == 2, f"INCORRECT ARG COUNT! Expected 2 got {len(sys.argv)}!"

    converter = MarkdownBBCodeConverter()
    print(converter.convert(sys.argv[1]))
