#-*- coding: utf-8 -*-

import logging
import logging.config
from typing import Any


class UpToInfoFilter(logging.Filter):
	def filter(self, record: logging.LogRecord) -> bool:
		return record.levelno <= logging.INFO


class ErrorColorFormatter(logging.Formatter):
	def format(self, record: logging.LogRecord) -> Any:
		result = super().format(record)
		return f'\033[1;31:40m{result}\033[0m'


LOGGER_NAME = "December"
LOGGER = logging.getLogger(LOGGER_NAME)
LOGGING_CONFIG = {
	"version": 1,
	"disable_existing_loggers": False,
	"formatters": {
		"simple": {
			"format": "[%(asctime)s][%(levelname)s] %(message)s",
			"datefmt": "%H:%M:%S"
		},
		"simple_red": {
			"()": ErrorColorFormatter,
			"format": "[%(asctime)s][%(levelname)s] %(message)s",
			"datefmt": "%H:%M:%S"
		},
		"detailed": {
			"format": "%(asctime)s | %(threadName)s | %(filename)sL%(lineno)s | %(levelname)s | %(message)s",
			"datefmt": "%Y-%m-%dT%H:%M:%S%z",
		}
	},
	"filters": {
		"up_to_info": {
			"()": UpToInfoFilter
		}
	},
	"handlers": {
		"console_error": {
			"class": "logging.StreamHandler",
			"level": "WARNING",
			"formatter": "simple_red",
			"stream": "ext://sys.stderr"
		},
		"console": {
			"class": "logging.StreamHandler",
			"level": "DEBUG",
			"formatter": "simple",
			"filters": ["up_to_info"],
			"stream": "ext://sys.stdout"
		},
		"file": {
			"class": "logging.handlers.RotatingFileHandler",
			"level": "DEBUG",
			"formatter": "detailed",
			"filename": "",
			"maxBytes": 1_000_000,
			"backupCount": 1
		}
	},
	"loggers": {
		LOGGER_NAME: {}
	},
	"root": {
		"level": "INFO",
		"handlers": [
			"console",
			"console_error",
			"file"
		]
	}
}

def setup_logging(log_file: str, level: int) -> None:
	LOGGING_CONFIG["handlers"]["file"]["filename"] = log_file
	logging.config.dictConfig(LOGGING_CONFIG)
	logging.getLogger().setLevel(level)
	return
