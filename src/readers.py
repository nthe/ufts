import csv
import json
from io import TextIOWrapper
from typing import Generator, Protocol


class Reader(Protocol):
    extention: str

    def read(self, f: TextIOWrapper) -> Generator: ...
    def get_mapping(self, o: dict | str) -> dict | None: ...


class JsonReader(Reader):
    extention = "json"

    def read(self, f: TextIOWrapper) -> Generator:
        yield from json.load(f)

    def get_mapping(self, o: dict | str) -> dict | None:
        if isinstance(o, dict):
            return {k: k for k in o.keys()}
        if isinstance(o, str):
            return None
        raise ValueError("Invalid object")


class JsonlReader(JsonReader):
    extention = "jsonl"

    def read(self, f: TextIOWrapper) -> Generator:
        yield from (json.loads(l) for l in f)


class CsvReader(Reader):
    extention = "csv"

    def read(self, f: TextIOWrapper) -> Generator:
        sniffer = csv.Sniffer()
        sample = "\n".join(f.readline() for _ in range(3))
        has_header = sniffer.has_header(sample)
        delimiter = sniffer.sniff(sample).delimiter

        f.seek(0)
        reader = csv.reader(f, delimiter=delimiter)
        if has_header:
            header = next(reader)
        else:
            header = [f"col_{i}" for i in range(len(next(reader)))]

        f.seek(0)
        yield from csv.DictReader(f, fieldnames=header, delimiter=delimiter)

    def get_mapping(self, o: dict) -> dict | None:
        if isinstance(o, dict):
            return {k: k for k in o.keys()}
        raise ValueError("Invalid object")


class TxtReader(Reader):
    extention = "txt"

    def read(self, f: TextIOWrapper) -> Generator:
        yield from f

    def get_mapping(self, _: dict | str) -> dict | None:
        return None


class LogReader(TxtReader):
    extention = "log"


register: list[type[Reader]] = [
    TxtReader,
    LogReader,
    JsonReader,
    JsonlReader,
    CsvReader,
]


def find_reader(ext: str) -> type[Reader]:
    ext = ext.lstrip(".")
    if reader := next(
        (r for r in register if r.extention == ext),
        None,
    ):
        return reader
    raise ValueError(f"Unsupported file extention: {ext}")
