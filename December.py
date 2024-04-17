#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import logging
import os
from time import sleep

from actions import action

#--------------------
#Settings
vars = {
	#ff locations
	'ffmpeg': './bin/ffmpeg',
	'ffprobe': './bin/ffprobe',

	#files
	'log_file': './December.log',
	'queue_file': './December.queue',
	'error_file': './December.error',

	#project variables
	'check_interval': 30,
	'subtitle_filter': ('.srt','.ass'),
	'media_filter': ('.mkv','.mp4','.mov','.m4v','.mpg','.mpeg','.avi','.flv','.webm','.wmv','.vob','.evo','.iso','.m2ts','.ts'),

	#logging
	'logging_level': logging.INFO,
	'logger': logging,

	#action-specific variables (only needed when action is used):
	#plex_scan
	'plex_baseurl': '',
	'plex_api_token': '',

	'sonarr_baseurl': '',
	'sonarr_api_token': '',
	'radarr_baseurl': '',
	'radarr_api_token': ''
}
#--------------------

vars = os.environ.get('December_vars', vars)
for file in ('ffmpeg','ffprobe','log_file', 'queue_file', 'error_file'):
	vars[file] = os.path.join(os.path.dirname(__file__), vars[file])
logging.basicConfig(level=vars['logging_level'], filename=vars['log_file'], format='[%(asctime)s][%(levelname)s]%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
if vars['logging_level'] == logging.DEBUG:
	vars['check_interval'] = 5
action = action(vars)

#--------------------
#Processing definition
media_process = [

]

subtitle_process = [

]
#--------------------

def remove_from_queue(file: str):
	result = []

	with open(vars['queue_file'], 'r') as f:
		queue = f.read().strip().split('\n')

	with open(vars['queue_file'], 'w+') as f:
		for entry in queue:
			if entry.strip() != file:
				result.append(entry.strip())
				f.write(entry.strip() + '\n')
	return result

def add_to_queue(file: str):
	with open(vars['queue_file'],'a') as f:
		f.write(file + '\n')
	return

def process(type: str, files: list):
	#get processing chain for file type
	chain = media_process if type == 'media' else subtitle_process
	#loop through every entry in the chain
	for link in chain:
		#check if entry is valid
		if not ('action' in link.keys() or 'arguments' in link.keys()):
			logging.error(' Action or link missing from an action in process list')
			return

		#note action and arguments of the entry
		method = link['action']
		args = link['arguments']
		func_name = f'[{method.__name__}]'

		#execute action (note returned file(s) and parse it/them to next function)
		logging.info(f'{func_name} Starting')
		logging.debug(f'{func_name} Received arguments are {args}')
		logging.debug(f'{func_name} Received files are {files}')
		files = method(func_name, files, **args)

		if files[0] == 'ERROR':
			if len(files) == 2:
				with open(vars['error_file'],'a') as f:
					f.write(files[1] + '\n')
			break

def setup_files():
	if not os.path.isfile(vars['queue_file']):
		open(vars['queue_file'], 'w+').close()
	if not os.path.isfile(vars['log_file']):
		open(vars['log_file'], 'w+').close()

if __name__ == '__main__':
	#handle sonarr and radarr connection
	if os.environ.get('radarr_eventtype') == 'Test':
		exit(0)
	elif os.environ.get('sonarr_eventtype') == 'Test':
		exit(0)
	elif os.environ.get('radarr_moviefile_path') != None:
		if not os.path.isfile(os.environ.get('radarr_moviefile_path')):
			logging.error('File does not exist')
			exit(1)
		add_to_queue(os.environ.get('radarr_moviefile_path'))
		exit(0)
	elif os.environ.get('sonarr_episodefile_path') != None:
		if not os.path.isfile(os.environ.get('sonarr_episodefile_path')):
			logging.error('File does not exist')
			exit(1)
		add_to_queue(os.environ.get('sonarr_episodefile_path'))
		exit(0)

	while True:
		#check if files (still) exist
		setup_files()

		#empty log file when line count surpasses 100.000
		with open(vars['log_file'],'r') as f:
			if len(f.read().split('\n')) > 100000:
				open(vars['log_file'],'w').close()

		#get file from queue
		with open(vars['queue_file'],'r') as f:
			file = str(f.readline().strip())

		#if queue is empty, sleep {interval} and check again
		if file in ('', None):
			sleep(vars['check_interval'])
		else:
			#'file' contains a complete file path to media file or subtitle
			try:
				logging.info(f' Processing {file}')
				if not os.path.isfile(file):
					logging.error(' File does not exist')
				else:
					#file exists
					if file.endswith(vars['subtitle_filter']):
						#file is a subtitle file
						process('subtitle', [file])

					elif file.endswith(vars['media_filter']):
						#file is a media file
						process('media', [file])

					else:
						#file not supported
						logging.warning(' File is not supported and thus ignored')

			except Exception as e:
				#an error occured
				logging.exception(' Something went wrong')
				#add the file to the error list
				with open(vars['error_file'], 'a') as f:
					f.write(file + '\n')

			#remove file from queue
			remove_from_queue(file)
