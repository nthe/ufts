from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Sequence

from .defs import SQLiteDefinition


@dataclass
class SearchEngine:
    db: sqlite3.Connection
    sqls: SQLiteDefinition
    name: str

    @classmethod
    def create(cls, *, name: str, at: Path) -> SearchEngine:
        path = at / f"{name}.db"
        db = sqlite3.connect(path)
        sqls = SQLiteDefinition.of(table=name, columns=["text"])
        db.executescript(sqls.pragma.query)
        db.executescript(sqls.create_table.query)
        return cls(db, sqls, name)

    def index(self) -> SearchEngine:
        self.db.executescript(self.sqls.create_index.query)
        self.db.executescript(self.sqls.index_table.query)
        self.db.executescript(self.sqls.create_triggers.query)
        return self

    def ingest(self, texts: Sequence[str]) -> SearchEngine:
        self.db.execute("begin")
        self.db.executemany(self.sqls.insert_into_table.query, [(t,) for t in texts])
        self.db.commit()
        return self

    def search(self, query: str, size: int = 5) -> Generator[str]:
        query = re.sub("[^0-9a-zA-Z]+", " ", query)
        terms = " OR ".join(query.split())
        results = self.db.execute(
            self.sqls.select.query,
            [terms, size],
        ).fetchmany(
            size=size,
        )
        yield from results
