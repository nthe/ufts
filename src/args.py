import argparse


def parse():
    parser = argparse.ArgumentParser(
        prog="uFTS",
        description="Micro Full-Text Search Engine",
    )
    parser.add_argument(
        "-d",
        "--dir",
        default=".",
        help="Directory to index",
    )
    parser.add_argument(
        "-g",
        "--glob",
        default="**/*.*",
        help="Glob pattern",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "jsonl", "text"],
        default="json",
        help="Input format",
    )
    return parser.parse_args()
