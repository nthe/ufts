import sys
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import wrap

from . import args
from .colors import Colored as cprint
from .engine import SearchEngine
from .utils import Timer


def cli():

    cprint.yellow(" * | micro full-text search engine")
    # conf = args.parse()
    # conf.dir = Path(conf.dir)
    # for f in Path(conf.dir).glob(conf.glob):
    #     print(f.suffix.lstrip("."))

    with open(sys.argv[1]) as f:
        data = json.load(f)
        data = list(set(data))

    with TemporaryDirectory(prefix="ufts_", dir=".") as tmp:
        cprint.blue(f" i | indexing {len(data):,} records")
        with Timer() as t:
            engine = SearchEngine.create(name="utfs", at=Path(tmp))
            engine.ingest(data)
            engine.index()
        cprint.blue(f" i | done in {t.elapsed:^8.4f} s")

        while True:
            query = input(" ? | ")
            if not query or query.lower() in {"q", "quit"}:
                break

            with Timer() as t:
                results = engine.search(query, size=5)

            for i, (rank, doc) in enumerate(results, start=1):
                cprint.green(f" {i} | {abs(float(rank)):^6.3f}", end=" ")
                cprint.white(
                    "\n".join(
                        wrap(
                            text=doc.strip(),
                            width=64,
                            subsequent_indent=" " * 12,
                        )
                    )
                )

            cprint.blue(f" i | done in {t.elapsed:^8.6f} s")

        cprint.blue(" i | bye")
