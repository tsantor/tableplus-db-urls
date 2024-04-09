import configparser
import logging
import shutil
from pathlib import Path

import pkg_resources

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


def copy_file(filename, dst):
    """Copy data files from data folder."""
    # Create destination dir if needed
    dir_path = Path(dst).parent
    if not dir_path.is_dir():
        dir_path.mkdir()

    # Copy data file to destination
    src = pkg_resources.resource_filename("tableplus", f"data/{filename}")
    dst = str(Path(dir_path).expanduser())
    shutil.copy2(src, dst)


CONFIG_FILE = Path("~/.tableplus/tableplus.cfg").expanduser()
if not CONFIG_FILE.exists():
    copy_file("tableplus.cfg", str(CONFIG_FILE))

LOG_FILE = Path("~/.tableplus/tableplus.log").expanduser()
if not LOG_FILE.exists():
    LOG_FILE.touch()

# -----------------------------------------------------------------------------


config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Default
SENTRY_DSN = config.get("default", "sentry_dsn", fallback=None)
