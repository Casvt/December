#-*- coding: utf-8 -*-

from time import sleep
from typing import Union

from backend.config import Config
from backend.helpers import BaseEnum
from backend.queue import Queue
from os.path import isfile

class Command(BaseEnum):
	CONFIG_UPDATE = "CONFIG_UPDATE"
	RESTART = "RESTART"
	SHUTDOWN = "SHUTDOWN"


class QueueHandler:
	stop_reason: Union[None, Command] = None

	def __init__(self) -> None:
		self.config_manager = Config()
		self.config = self.config_manager.config
		self.queue = Queue()
		return

	def __handle_command(self, command: Command) -> None:
		if command == Command.CONFIG_UPDATE:
			self.config_manager.reload_config()

		elif command in (Command.RESTART, Command.SHUTDOWN):
			self.stop_reason = command

		return

	def __handle_file(self, file: str) -> None:
		try:
			self.config.logger.info(f'Processing {file}')

			if file.endswith(self.config.subtitle_filter):
				# File is a subtitle file
				pass

			elif file.endswith(self.config.media_filter):
				# File is a media file
				pass

			else:
				self.config.logger.warning("File is not supported or allowed")

		except Exception as e:
			self.config.logger.exception('Something went wrong: ')

			# Add the file to the error list
			with open(self.config.error_file, 'a') as f:
				f.write(file + '\n')

		self.config.logger.info(f'Finished {file}')

		return

	def run(self) -> Union[None, Command]:
		try:
			while not self.stop_reason:
				row = self.queue.get()

				if row is None:
					# Queue empty
					sleep(self.config.check_interval)

				elif isfile(row):
					# Process file
					self.__handle_file(row)
					self.queue.remove(row)

				else:
					try:
						command = Command(row)
					except ValueError:
						# Not an empty row, file or command
						self.config.logger.error(f"Unknown command or not a file: {row}")
					else:
						# Handle command
						self.__handle_command(command)

					self.queue.remove(row)

		except (SystemExit, KeyboardInterrupt):
			self.stop_reason = Command.SHUTDOWN

		return self.stop_reason
