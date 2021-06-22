import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from colorama import init, Fore, Back, Style

init()  # For Windows

# Add level log 'success'
logging.addLevelName(45, "SUCCESS")


class BaseDiscordTimedRotatingFileHandler(TimedRotatingFileHandler):
	def __init__(self, *args, extension: str = 'log', datefmt: str = "%Y%m%d", **kwargs):

		super().__init__(*args, **kwargs)
		self.extension = extension
		self.datefmt = datefmt

	def rotatation_filename(default_name):
		dt = datetime.now().strftime(self.datefmt)
		return f"{self.filename}_{dt}.{self.extension}"



COLORS = {
	"success": Fore.GREEN,
	"critical": Fore.RED,
	"exception": Fore.RED,
	"error": Fore.RED,
	"warning": Fore.YELLOW,
	"info": Fore.WHITE,
	"debug": Fore.BLUE
}


class ColoredFormatter(logging.Formatter):
	def __init__(self, *args, use_color = True, **kwargs):
		super().__init__(*args, **kwargs)
		self.use_color = use_color

	def format(self, record):
		msg = super().format(record)

		levelname = record.levelname
		if self.use_color and levelname.lower() in COLORS.keys():
			msg =  COLORS[levelname.lower()] + msg + Style.RESET_ALL
		return msg


class BaseDiscordLogger(logging.Logger):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def success(self, msg: str, *args, **kwargs):
		self.log(45, msg, *args, **kwargs)