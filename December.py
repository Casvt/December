#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from argparse import ArgumentParser
from os import environ, execv
from os.path import abspath, isfile
from sys import argv
from typing import NoReturn, Union

from backend.config import Config
from backend.handler import Command, QueueHandler
from backend.helpers import check_python_version
from backend.queue import Queue


def December(config_file: str) -> Union[None, NoReturn]:
	if not check_python_version():
		exit(1)

	config_manager = Config(config_file)
	config = config_manager.config

	for t in ('radarr_eventtype', 'sonarr_eventtype'):
		if environ.get(t) == 'Test':
			exit(0)

	queue = Queue(config.queue_file)

	for t in ('radarr_moviefile_path', 'sonarr_episodefile_path'):
		path = environ.get(t)
		if path is not None:
			if not isfile(path):
				config.logger.error("File does not exist")
				exit(1)
			queue.add(path)
			exit(0)

	queue_handler = QueueHandler()
	stop_reason = queue_handler.run()

	if stop_reason == Command.RESTART:
		config.logger.info('Restarting')
		execv(abspath(__file__), argv)

	return

if __name__ == '__main__':
	parser = ArgumentParser(description="An automatic file transcoder following the rules you set")
	parser.add_argument('-c', '--Config', type=str, required=True, help="Path to the configuration file")
	args = parser.parse_args()

	December(args.Config)
