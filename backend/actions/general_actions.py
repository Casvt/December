#-*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Type, Union


@dataclass
class ActionEntry:
	action: str
	vars: Dict[str, Any]
	
	def __post_init__(self):
		if not isinstance(self.action, str):
			raise TypeError
		if not isinstance(self.vars, dict):
			raise TypeError
		return


class ActionVars:
	pass


class Action(ABC):
	var_class: Union[Type[ActionVars], None] = None
	
	def __init__(self, vars: Union[ActionVars, None]) -> None:
		self.vars = vars
		return

	@abstractmethod
	def run(self, files: List[str]) -> List[str]:
		return

	def __repr__(self) -> str:
		return f'{self.__class__.__name__}(vars={self.vars})'
