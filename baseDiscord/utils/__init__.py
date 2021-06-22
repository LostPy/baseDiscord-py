import logging as __logging

from . import manage_messages
from . import checks
from . import logging


def new_logger(name: str, *,
	fmt: str = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
	datefmt: str = "%Y-%m-%d %H:%M:%S",
	level: int = __logging.DEBUG,
	file: str = None,
	frequency: str = None,
	count: int = 7
) -> __logging.Logger:
	"""Create a new logger

	Parameters
	----------
	name : str
		The logger name
	OPTIONAL[fmt] : str
		Log messages format to use
		Default: "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"
	OPTIONAL[datefmt] : str
		The date format
		Default: "%Y-%m-%d %H:%M:%S"
	OPTIONAL[level] : int
		The level logger
		Default: logging.DEBUG (10)
	OPTIONAL[file] : str
		The path of file if you want save logs in the file. If `frequency` is used, file is a model for files path.
		Default: None
	OPTIONAL[frequency] : str
		The time frequency to logs files if you want a rotation logs files.
		Default: None
	OPTIONAL[count] : int
		Used if `frequency` is not None. The number of file in the rotation.
		Default: 7
	"""
	logger = __logging.getLogger(name=name)

	logger.setLevel(level)
	return logger


__logger_baseBot = new_logger("BaseBot", level=__logging.DEBUG)