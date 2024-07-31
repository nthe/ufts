import sys
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from . import args
from .colors import Colored as cprint
from .engine import SearchEngine
from .utils import catchtime


def cli():

    # conf = args.parse()
    # conf.dir = Path(conf.dir)
    # for f in Path(conf.dir).glob(conf.glob):
    #     print(f.suffix.lstrip("."))

    # return
    with open(sys.argv[1]) as f:
        data = json.load(f)
        data = list(set(data))

    with TemporaryDirectory(prefix="ufts_", dir=".") as tmp:
        cprint.blue(f"[i] indexing {len(data):,} docs")
        with catchtime() as t:
            engine = SearchEngine.create(name="test", at=Path(tmp))
            engine.ingest(data)
            engine.index()
        cprint.blue(f"[i] done in {float(t):>6.2f} seconds")
        cprint.blue(f"[i] ready")

        while True:
            query = input("\n(Q) ")
            if not query or query.lower() in {"q", "quit"}:
                break

            with catchtime() as t:
                results = engine.search(query)

            for i, (rank, doc) in enumerate(results, start=1):
                cprint.green(f"    [{i}] ({abs(float(rank)):>6.2f})", end=" ")
                cprint.white(doc.strip()[:96], end="")
                cprint.white("..." if len(doc) > 96 else "")

            cprint.blue(f"[i] took {float(t):>6.2f} seconds")

        cprint.blue("[i] bye")
