# author@alingse
# 2015.10.09

import csv
import io
import json
from typing import Any

import xlwt

from jsoncsv.utils import JsonType


class Dump:
    def __init__(self, fin: io.TextIOBase, fout: io.TextIOBase | io.BytesIO, **kwargs: Any) -> None:
        self.fin = fin
        self.fout = fout
        self.initialize(**kwargs)

    def initialize(self, **kwargs: Any) -> None:
        pass

    def prepare(self) -> None:
        pass

    def dump_file(self) -> None:
        raise NotImplementedError

    def on_finish(self) -> None:
        pass

    def dump(self) -> None:
        self.prepare()
        self.dump_file()
        self.on_finish()


class ReadHeadersMixin:
    @staticmethod
    def load_headers(
        fin: io.TextIOBase,
        read_row: int | None = None,
        sort_type: bool | None = None,  # noqa: ARG004 - reserved for future use
    ) -> tuple[list[str], list[dict[str, JsonType]]]:
        headers: set[str] = set()
        datas: list[dict[str, JsonType]] = []

        # read
        if not read_row or read_row < 1:
            read_row = -1

        for line in fin:
            obj = json.loads(line)
            assert isinstance(obj, dict)
            headers.update(obj.keys())
            datas.append(obj)

            read_row -= 1
            if not read_row:
                break
        # TODO: add some sort_type here
        headers_list = sorted(headers)

        return (headers_list, datas)


class DumpExcel(Dump, ReadHeadersMixin):
    def initialize(self, **kwargs: Any) -> None:
        super().initialize(**kwargs)
        self._read_row = kwargs.get("read_row")
        self._sort_type = kwargs.get("sort_type")

    def prepare(self) -> None:
        headers, datas = self.load_headers(self.fin, self._read_row, self._sort_type)
        self._headers = headers
        self._datas = datas

    def write_headers(self) -> None:
        raise NotImplementedError

    def write_obj(self, obj: dict[str, JsonType]) -> None:
        raise NotImplementedError

    def dump_file(self) -> None:
        self.write_headers()

        for obj in self._datas:
            self.write_obj(obj)

        for line in self.fin:
            obj = json.loads(line)
            assert isinstance(obj, dict)
            self.write_obj(obj)


class DumpCSV(DumpExcel):
    def initialize(self, **kwargs: Any) -> None:
        super().initialize(**kwargs)
        self.csv_writer: csv.DictWriter[str] | None = None

    def write_headers(self) -> None:
        assert isinstance(self.fout, io.TextIOBase)
        self.csv_writer = csv.DictWriter(self.fout, self._headers)
        self.csv_writer.writeheader()

    def write_obj(self, obj: dict[str, JsonType]) -> None:
        patched_obj: dict[str, str] = {key: self.patch_value(value) for key, value in obj.items()}
        assert self.csv_writer is not None
        self.csv_writer.writerow(patched_obj)

    def patch_value(self, value: JsonType) -> str:
        if value in (None, {}, []):
            return ""
        return str(value)


class DumpXLS(DumpExcel):
    def initialize(self, **kwargs: Any) -> None:
        super().initialize(**kwargs)

        self.sheet = kwargs.get("sheet", "Sheet1")
        self.wb = xlwt.Workbook(encoding="utf-8")
        self.ws = self.wb.add_sheet(self.sheet)
        self.row = 0
        self.cloumn = 0

    def write_headers(self) -> None:
        for head in self._headers:
            self.ws.write(self.row, self.cloumn, head)
            self.cloumn += 1
        self.row += 1

    def write_obj(self, obj: dict[str, JsonType]) -> None:
        self.cloumn = 0

        for head in self._headers:
            value = obj.get(head)
            # patch
            if value == {}:
                value = "{}"
            self.ws.write(self.row, self.cloumn, value)
            self.cloumn += 1

        self.row += 1

    def on_finish(self) -> None:
        assert isinstance(self.fout, io.BufferedIOBase)
        self.wb.save(self.fout)


def dump_excel(
    fin: io.TextIOBase,
    fout: io.TextIOBase | io.BytesIO,
    klass: type[DumpExcel],
    **kwargs: Any,
) -> None:
    if not isinstance(klass, type) or not issubclass(klass, DumpExcel):
        raise ValueError("unknow dumpexcel type")

    dump = klass(fin, fout, **kwargs)
    dump.dump()
