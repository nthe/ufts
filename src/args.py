import argparse


def parse():
    parser = argparse.ArgumentParser(
        prog="uFTS",
        description="Micro Full-Text Search Engine",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose mode",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Input file",
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
    parser.add_argument(
        "-a",
        "--auto-or",
        action="store_true",
        help="Automatically convert search query to boolean OR terms",
    )
    parser.add_argument(
        "-m",
        "--metadata",
        action="store_true",
        help="Include metadata in search results",
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Clean query from special characters",
    )
    return parser.parse_args()
