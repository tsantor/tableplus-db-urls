import argparse
import logging
import sys

from . import __version__
from .core import run as cli_run

# from .logging import setup_logging

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


def get_parser():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate TablePlus DB URLs from CookieCutter Django to make setting up connections easier."
    )
    parser.add_argument("-p", "--path", required=True, help="Path to the project")
    parser.add_argument("--user", required=True, help="SSH User")
    parser.add_argument("--host", required=True, help="SSH Host")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument("--version", action="version", version=__version__)

    return parser.parse_args()


def run():
    """Run script."""

    args = get_parser()

    # setup_logging(args.verbose)

    cli_run(args)

    sys.exit()


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run()
