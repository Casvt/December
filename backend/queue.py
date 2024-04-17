#-*- coding: utf-8 -*-

from typing import Union

from backend.helpers import Singleton


class Queue(metaclass=Singleton):
	def __init__(self, queue_file: str = '') -> None:
		self.file = queue_file

	def get(self) -> Union[str, None]:
		with open(self.file, 'r') as f:
			row = f.readline().strip() or None
		return row

	def add(self, entry: str) -> None:
		with open(self.file, 'a') as f:
			f.write(entry.rstrip() + '\n')
		return

	def remove(self, entry: str) -> None:
		with open(self.file, 'r') as f:
			queue = [e.rstrip() for e in f.readlines()]
			queue.remove(entry.rstrip())
		with open(self.file, 'w+') as f:
			f.write(r'\n'.join(queue))
		return
