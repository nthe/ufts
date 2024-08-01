import sys
import json
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import wrap

from . import args
from .colors import ColorCodes, Colored as cprint
from .engine import SearchEngine
from .utils import Timer


def cli():

    cprint.yellow(" * | micro full-text search engine")
    conf = args.parse()
    # conf.dir = Path(conf.dir)
    # for f in Path(conf.dir).glob(conf.glob):
    #     print(f.suffix.lstrip("."))

    with open(conf.input) as f:
        data = json.load(f)
        data = list(set(data))

    with TemporaryDirectory(prefix="ufts_", dir=".") as tmp:
        cprint.blue(f" i | indexing {len(data):,} records", disabled=not conf.verbose)
        with Timer() as t:
            engine = SearchEngine.create(name="utfs", columns=["content"], at=Path(tmp))
            engine.ingest(data)
            engine.index()
        cprint.blue(f" i | done in {t.elapsed:^8.4f} s", disabled=not conf.verbose)

        while True:
            query = input(" ? | ").strip()
            if not query or query.lower() in {"q", "quit"}:
                break

            if conf.clean:
                clean_query = engine.sanitize(query)

            if conf.auto_or:
                clean_query = " OR ".join(c for c in clean_query.split(" ") if c)

            try:
                with Timer() as t:
                    cprint.blue(
                        f" i | searching for {clean_query!r}", disabled=not conf.verbose
                    )
                    results = engine.search(clean_query, size=5)

                for i, (rank, doc, _) in enumerate(results, start=1):
                    doc = doc.replace("<b>", ColorCodes.BOLD)
                    doc = doc.replace("</b>", ColorCodes.END)
                    cprint.green(f" {i} | {abs(float(rank)):^6.3f}", end=" ")
                    cprint.white(
                        "\n".join(
                            wrap(
                                text=doc.strip(),
                                width=72,
                                subsequent_indent=" " * 12,
                            )
                        )
                    )

            except sqlite3.Error as e:
                err_name = e.sqlite_errorname
                err_code = e.sqlite_errorcode
                err_type = e.__class__.__name__
                cprint.red(f" ! | {err_type}, {err_name}, code {err_code}")
                cprint.red(f" ! | {e}")
                cprint.red(f" ! | query: {query!r}")
                cprint.red(f" ! | clean query: {clean_query!r}")

            cprint.blue(f" i | done in {t.elapsed:^8.6f} s", disabled=not conf.verbose)

        cprint.blue(" i | bye")
