#-*- coding: utf-8 -*-

from enum import Enum
from sys import version_info
from typing import Any, Dict, TypeVar

T = TypeVar('T')

def check_python_version() -> bool:
	"""Check if the python version that is used is a minimum version.

	Returns:
		bool: Whether or not the python version is version 3.8 or above or not.
	"""
	if not (version_info.major == 3 and version_info.minor >= 8):
		from backend.logging import LOGGER
		LOGGER.critical(
			'The minimum python version required is python3.8 ' +
			'(currently ' + str(version_info.major) + '.' + str(version_info.minor) + '.' + str(version_info.micro) + ').'
		)
		return False
	return True


class Singleton(type):
	_instances: Dict[str, Any] = {}

	def __call__(cls, *args, **kwargs):
		if cls.__name__ not in cls._instances:
			cls._instances[cls.__name__] = super().__call__(*args, **kwargs)

		return cls._instances[cls.__name__]

class BaseEnum(Enum):
	def __eq__(self, other: object) -> bool:
		return self.value == other

	def __hash__(self) -> int:
		return id(self.value)
