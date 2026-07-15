"""Generic Conversion Module

A base module with base classes to use for making converter scripts

    Architecture by Errorbot1122, Code by Errorbot1122 & Gemini
"""

import re
from typing import Any, Optional, Protocol


# -- Protocols --
class Parser(Protocol):
    def parse(self, text: str) -> Optional[tuple[Any, ...]]: ...


class Handler(Protocol):
    def handle(self, text: str, *args: Any, **kwargs: Any) -> str: ...

    @classmethod
    def _slice_replace(cls, text: str, start: int, end: int, replacement: str) -> str:
        """Centralized helper function managing clean range slicing substitutions."""
        return text[:start] + replacement + text[end:]


# -- Shielding Code --
class _ShieldStore:
    def __init__(self) -> None:
        self.data: dict[str, tuple[tuple[Any, ...], dict[str, Any]]] = {}
        self.counter = 0


class _InternalShieldHandler(Handler):
    def __init__(self, store: _ShieldStore, prefix: str) -> None:
        self.store = store
        self.prefix = prefix

    def handle(
        self, text: str, start_idx: int, end_idx: int, *args: Any, **kwargs: Any
    ) -> str:
        key = f"\x02SHIELD{self.prefix}C{self.store.counter}\x03"
        self.store.counter += 1

        self.store.data[key] = (args, kwargs)
        return self._slice_replace(text, start_idx, end_idx, key)


class _InternalUnshieldParser(Parser):
    def __init__(self, prefix: str) -> None:
        self._pattern = re.compile(rf"\x02SHIELD{re.escape(prefix)}C(\d+)\x03")

    def parse(self, text: str) -> Optional[tuple[int, int, str]]:
        match = self._pattern.search(text)
        if not match:
            return None
        return match.start(), match.end(), match.group(0)


class _InternalUnshieldHandler(Handler):
    def __init__(self, store: _ShieldStore, handler: Optional[Handler] = None) -> None:
        self.store = store
        self.handler = handler

    def handle(self, text: str, start_idx: int, end_idx: int, key: str) -> str:
        if key not in self.store.data:
            return text

        args, kwargs = self.store.data[key]
        if self.handler is None:
            replacement = args[0] if args else ""
        else:
            return self.handler.handle(text, start_idx, end_idx, *args, **kwargs)
        return self._slice_replace(text, start_idx, end_idx, replacement)


# -- Converter Core Pipeline Engine --
class Convert:
    def __init__(self, parser: Parser, handler: Handler) -> None:
        self.parser = parser
        self.handler = handler

    def run(self, text: str) -> Optional[str]:
        parse_result = self.parser.parse(text)
        if parse_result is None:
            return None

        start, end, *args = parse_result
        return self.handler.handle(text, start, end, *args)


class Converter:
    def __init__(self) -> None:
        self.converts: dict[int, list[Convert]] = {}
        self._shield_types_count = 0

    def add_convert(self, parser: Parser, handler: Handler, order: int = 0):
        """Registers a rule into a specific execution phase order layer (defaults to 0)."""
        if order not in self.converts:
            self.converts[order] = []
        self.converts[order].append(Convert(parser, handler))

    def add_shield(
        self,
        parser: Parser,
        shield_order: int,
        unshield_order: int,
        unshield_handler: Optional[Handler] = None,
    ) -> None:
        """Automates safe data isolation by shielding text at one phase and restoring it at another."""
        store = _ShieldStore()
        prefix = f"TYPE{self._shield_types_count}"
        self._shield_types_count += 1

        self.add_convert(
            parser, _InternalShieldHandler(store, prefix), order=shield_order
        )

        self.add_convert(
            _InternalUnshieldParser(prefix),
            _InternalUnshieldHandler(store, unshield_handler),
            order=unshield_order,
        )

    def convert(self, text: str) -> str:
        for order in sorted(self.converts.keys()):
            changed = True
            while changed:
                changed = False
                for convert in self.converts[order]:
                    current_text = convert.run(text)
                    if current_text is not None:
                        text = current_text
                        changed = True
                        break

        return text
