import logging
from rich.traceback import install
from rich.logging import RichHandler

# logger init
FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rich")

# metadata 
__version__ = "0.0.1"

# handle traceback with rich support
install()