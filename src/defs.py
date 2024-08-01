from __future__ import annotations

from collections import UserString
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


class SQLQuery(UserString):

    @property
    def query(self) -> str:
        return self.data

    @classmethod
    def of(cls, path: Path | str) -> SQLQuery:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"{path} not found")
        return cls(path.read_text())

    def format(self, *args: Any, **kwargs: Any) -> SQLQuery:
        return SQLQuery(self.data.format(*args, **kwargs))

    def format_map(self, mapping: Mapping[str, Any]) -> SQLQuery:
        return SQLQuery(self.data.format_map(mapping))


@dataclass
class SQLiteDefinition:
    table_name: str
    index_name: str
    columns: list[str]
    create_table: SQLQuery
    create_index: SQLQuery
    create_triggers: SQLQuery
    index_table: SQLQuery
    insert_into_table: SQLQuery
    select: SQLQuery
    pragma: SQLQuery

    @classmethod
    def of(
        cls,
        table: str,
        columns: list[str],
    ) -> SQLiteDefinition:

        index_name = f"{table}_fts_idx"

        format_kwargs = {
            "table": table,
            "fts_idx": index_name,
            "cols": ", ".join(columns),
            "params": ", ".join("?" for _ in columns),
            "new_cols": ", ".join(f"new.{c}" for c in columns),
            "old_cols": ", ".join(f"old.{c}" for c in columns),
        }

        def load_and_format(path: Path | str) -> SQLQuery:
            return SQLQuery.of(path).format_map(format_kwargs)

        return cls(
            table_name=table,
            index_name=index_name,
            columns=columns,
            pragma=load_and_format("./src/ddl/pragma.sql"),
            create_table=load_and_format("./src/ddl/table.sql"),
            create_index=load_and_format("./src/ddl/index.sql"),
            create_triggers=load_and_format("./src/ddl/triggers.sql"),
            index_table=load_and_format("./src/dml/populate.sql"),
            insert_into_table=load_and_format("./src/dml/insert.sql"),
            select=load_and_format("./src/dql/select.sql"),
        )
