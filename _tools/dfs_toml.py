# Script *mostly* Written by ChatGPT-5.5
from decimal import Decimal
import datetime
import sys

unicode = str


# #region From https://github.com/uiri/toml/blob/master/toml/encoder.py
def _dump_str(v):
    if sys.version_info < (3,) and hasattr(v, "decode") and isinstance(v, str):
        v = v.decode("utf-8")
    v = "%r" % v
    if v[0] == "u":
        v = v[1:]
    singlequote = v.startswith("'")
    if singlequote or v.startswith('"'):
        v = v[1:-1]
    if singlequote:
        v = v.replace("\\'", "'")
        v = v.replace('"', '\\"')
    v = v.split("\\x")
    while len(v) > 1:
        i = -1
        if not v[0]:
            v = v[1:]
        v[0] = v[0].replace("\\\\", "\\")
        # No, I don't know why != works and == breaks
        joinx = v[0][i] != "\\"
        while v[0][:i] and v[0][i] == "\\":
            joinx = not joinx
            i -= 1
        if joinx:
            joiner = "x"
        else:
            joiner = "u00"
        v = [v[0] + joiner + v[1]] + v[2:]
    return unicode('"' + v[0] + '"')


def _dump_float(v):
    return "{}".format(v).replace("e+0", "e+").replace("e-0", "e-")


def _dump_time(v):
    utcoffset = v.utcoffset()
    if utcoffset is None:
        return v.isoformat()
    # The TOML norm specifies that it's local time thus we drop the offset
    return v.isoformat()[:-6]


# #endregion


class DFSTomlEncoder:

    def __init__(self, dump_funcs=None):
        self.dump_funcs = {
            str: _dump_str,
            list: self.dump_list,
            bool: lambda value: str(value).lower(),
            int: lambda value: value,
            float: _dump_float,
            Decimal: _dump_float,
            datetime.datetime: lambda value: value.isoformat().replace("+00:00", "Z"),
            datetime.date: lambda value: value.isoformat(),
            datetime.time: _dump_time,
        }

        if dump_funcs:
            self.dump_funcs.update(dump_funcs)

    def dump_value(self, value):
        dump_func = next(
            (
                func
                for value_type, func in self.dump_funcs.items()
                if isinstance(value, value_type)
            ),
            None,
        )

        if dump_func is None:
            return _dump_str(str(value))

        return dump_func(value)

    def dump_list(self, values):
        result = "["

        for value in values:
            result += f" {self.dump_value(value)},"

        result += "]"
        return result

    def dumps(self, data):
        return self._dump_table(
            table=data,
            table_path="",
            visible_depth=0,
        ).lstrip("\n")

    def _dump_table(
        self,
        table,
        table_path,
        visible_depth,
    ):
        result = ""

        values = {}
        child_tables = {}
        array_tables = {}

        #
        # Split table contents
        #
        for key, value in table.items():

            if isinstance(value, dict):
                child_tables[key] = value

            elif (
                isinstance(value, list)
                and value
                and all(isinstance(item, dict) for item in value)
            ):
                array_tables[key] = value

            else:
                values[key] = value

        #
        # Only emit a section if it contains data.
        # Wrapper sections containing only child tables
        # are skipped entirely.
        #
        emit_header = bool(table_path) and (values or array_tables)

        if emit_header:

            indent = "    " * max(0, visible_depth)

            result += f"\n{indent}[{table_path}]\n"

            #
            # Fields always come first
            #
            for key, value in values.items():
                result += f"{indent}{key} = {self.dump_value(value)}\n"

            #
            # Arrays of tables next
            #
            for table_name, table_array in array_tables.items():

                array_path = f"{table_path}.{table_name}"

                for table_item in table_array:

                    result += f"\n{indent}[[{array_path}]]\n"

                    for item_key, item_value in table_item.items():

                        if isinstance(item_value, dict):
                            continue

                        result += (
                            f"{indent}{item_key} = {self.dump_value(item_value)}\n"
                        )

        #
        # Visible sections increase indentation depth.
        # Hidden wrapper sections do not.
        #
        next_depth = visible_depth + 1 if emit_header else visible_depth
        #
        # Child tables always come after fields.
        #
        for child_name, child_table in child_tables.items():

            child_path = f"{table_path}.{child_name}" if table_path else child_name

            result += self._dump_table(
                table=child_table,
                table_path=child_path,
                visible_depth=next_depth,
            )

        #
        # Nested tables inside arrays-of-tables
        #
        for table_name, table_array in array_tables.items():

            array_path = f"{table_path}.{table_name}"

            for table_item in table_array:

                for item_key, item_value in table_item.items():

                    if not isinstance(item_value, dict):
                        continue

                    child_path = f"{array_path}.{item_key}"

                    result += self._dump_table(
                        table=item_value,
                        table_path=child_path,
                        visible_depth=next_depth + 1,
                    )

        #
        # Root-level fields
        #
        if not table_path:

            root = ""

            for key, value in values.items():
                root += f"{key} = {self.dump_value(value)}\n"

            return root + result

        return result
