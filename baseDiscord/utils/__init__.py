import logging as __logging

from . import manage_messages
from . import checks
from . import logging


__logging.setLoggerClass(logging.BaseDiscordLogger)


def new_logger(name: str, *,
	fmt: str = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
	datefmt: str = "%Y-%m-%d %H:%M:%S",
	level: int = __logging.DEBUG,
	file: str = None,
	frequency: str = None,
	backupcount: int = 7
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
	OPTIONAL[backupcount] : int
		Used if `frequency` is not None. The number of backup to save in the rotation.
		Default: 7
	"""
	logger = __logging.getLogger(name=name)
	stream_formatter = logging.ColoredFormatter(fmt, datefmt=datefmt)
	file_formatter = __logging.Formatter(fmt, datefmt=datefmt)
	
	stream_handler = __logging.StreamHandler()
	if file and not frequency:
		file_handler = __logging.FileHandler(file, mode='a', encoding=None, delay=False)
	elif file and frequency:
		file_handler = logging.BaseDiscordTimedRotatingFileHandler(file, mode='a', extension="log", datefmt="%Y%m%d", when=frequency, backupcount=backupcount)
	else:
		file_handler = None

	stream_handler.setLevel(__logging.DEBUG)
	stream_handler.setFormatter(stream_formatter)
	logger.addHandler(stream_handler)
	
	if file_handler:
		file_handler.setLevel(__logging.WARNING)
		file_handler.setFormatter(file_formatter)
		logger.addHandler(file_handler)

	logger.setLevel(level)
	return logger


__logger_baseBot = new_logger("BaseBot", level=__logging.DEBUG)