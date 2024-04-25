#-*- coding: utf-8 -*-

from os.path import isfile
from time import perf_counter, sleep
from typing import Union

from backend.config import Config
from backend.helpers import BaseEnum
from backend.queue import Queue


class Command(BaseEnum):
	CONFIG_UPDATE = "CONFIG_UPDATE"
	RESTART = "RESTART"
	SHUTDOWN = "SHUTDOWN"


class QueueHandler:
	stop_reason: Union[None, Command] = None

	def __init__(self) -> None:
		self.config_manager = Config()
		self.queue = Queue()
		return

	def __handle_command(self, command: Command) -> None:
		if command == Command.CONFIG_UPDATE:
			self.config_manager.reload_config()

		elif command in (Command.RESTART, Command.SHUTDOWN):
			self.stop_reason = command

		return

	def __handle_file(self, file: str) -> None:
		config = self.config_manager.config
		try:
			config.logger.info(f'Processing {file}')

			if file.endswith((
				*config.media_filter,
				*config.subtitle_filter
			)):
				if file.endswith(config.media_filter):
					chain = config.media_process
				else:
					chain = config.subtitle_process
				
				start_time = perf_counter()
				files = [file]
				for link in chain:
					config.logger.info(f'Starting {link.__class__.__name__}')
					config.logger.debug(f'Running files: {files}')
					files = link.run(files)
				config.logger.debug(f'Resulting files: {files}')
				config.logger.debug(f'Total time: {perf_counter() - start_time:.2f}s')

			else:
				config.logger.warning("File is not supported or allowed")

		except Exception as e:
			config.logger.exception('Something went wrong: ')

			# Add the file to the error list
			with open(config.error_file, 'a') as f:
				f.write(file + '\n')

		config.logger.info(f'Finished {file}')

		return

	def run(self) -> Union[None, Command]:
		try:
			while not self.stop_reason:
				row = self.queue.get()

				if row is None:
					# Queue empty
					self.queue.remove('')
					sleep(self.config_manager.config.check_interval)

				elif isfile(row):
					# Process file
					self.__handle_file(row)
					self.queue.remove(row)

				else:
					try:
						command = Command(row)
					except ValueError:
						# Not an empty row, file or command
						self.config_manager.config.logger.error(
							f"Unknown command or not a file: {row}"
						)
					else:
						# Handle command
						self.__handle_command(command)

					self.queue.remove(row)

		except (SystemExit, KeyboardInterrupt):
			self.stop_reason = Command.SHUTDOWN

		return self.stop_reason
