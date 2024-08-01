import argparse


def parse():
    parser = argparse.ArgumentParser(
        prog="uFTS",
        description="Micro Full-Text Search Engine",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Input file",
        required=False,
    )
    parser.add_argument(
        "-a",
        "--auto-or",
        action="store_true",
        help="Automatically convert search query to boolean OR terms",
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Clean query from special characters",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose mode",
    )
    return parser.parse_args()
