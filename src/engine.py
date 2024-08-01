from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Iterable

from .defs import SQLiteDefinition


@dataclass
class SearchEngine:
    db: sqlite3.Connection
    sqls: SQLiteDefinition
    name: str
    mapping: dict[str, str] | None

    @classmethod
    def create(
        cls,
        *,
        name: str,
        at: Path,
        mapping: dict[str, str] | None = None,
    ) -> SearchEngine:
        path = at / f"{name}.db"
        db = sqlite3.connect(path)
        cols = ["content"]
        if mapping:
            cols = list(mapping.keys())
        sqls = SQLiteDefinition.of(table=name, columns=cols)
        db.executescript(sqls.pragma.query)
        db.executescript(sqls.create_table.query)
        return cls(db, sqls, name, mapping)

    def transform(self, obj):
        if not self.mapping:
            return [obj]
        return [obj.get(m, "") for m in self.mapping.values()]

    def ingest(self, items: Iterable) -> SearchEngine:
        self.db.execute("begin")
        self.db.executemany(
            self.sqls.insert_into_table.query,
            map(self.transform, items),
        )
        self.db.commit()
        return self

    def index(self) -> SearchEngine:
        self.db.executescript(self.sqls.create_index.query)
        self.db.executescript(self.sqls.index_table.query)
        self.db.executescript(self.sqls.create_triggers.query)
        return self

    @classmethod
    def sanitize(cls, query: str) -> str:
        return re.sub(r"[^0-9a-zA-Z\^\*\(\)\+\"]+", " ", query)

    def search(self, query: str, size: int = 5) -> Generator[dict]:
        cursor = self.db.execute(self.sqls.select.query, [query, size])
        headers = [c[0] for c in cursor.description]
        # FIXME: This is a hack to "rename" the highlight column
        headers[-1] = "highlight"
        results = cursor.fetchmany(size=size)
        for r in results:
            yield {h: r[i] for i, h in enumerate(headers)}
