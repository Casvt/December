#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
Documentation:
	Workings:
		When the script is run, a 'queue' file is created (if it didn't exist already).
		You, or any external software like sonarr/radarr, can then add absolute filepaths to this queue file.
		The entries in the queue are delimited by a newline ('\n'). The files in the queue will be processed
		one by one, going from top to bottom. There will also be a log file created, in which you can see 
		what is happening.

		Each file in the queue is processed individually. When a file is processed, it will first be checked
		at what type of file it is: 'media' or 'subtitle'. A media file contains a video stream (and maybe also
		a audio and/or subtitle stream) and a subtitle file is... a subtitle file.

		Depending on the file type, the file will be 'treated' differently. How a file is 'treated' can, of course,
		be defined in a so called 'process'. The two file types have their own process and thus are processed
		differently. Below, you can find 'media_process' and 'subtitle_process' in which you can define the so
		called 'actions' that can be applied to the files. A 'process' is the definition of a chain of 'actions'.

		Each action manipulates the files in a certain way. By making a chain of actions (the process for the file type),
		you can very precisely define what you want to happen to your files. How to setup these processes will be
		explained later in the documentation.

		To integrate this script into the 'automation flow', you must integrate the queue file into other softwares.
		E.G. Make a connection in Sonarr which appends the absolute filepath of a newly downloaded file to the queue
		file. This way, a newly downloaded file will automatically be processed and manipulated.

		This software is intended to run as a service. That means that this isn't supposed to be run 
		"once in a while by the user". Instead, this script should be run constantly in the background. It will 
		automatically scan the queue and process new entries. When the queue is empty, it will wait and scan every 
		once in a while to see if a file is added to the queue (the check interval can be defined in the vars dict 
		at 'check_interval'). It is an endlessly running script that does what it needs to do when it needs to do it.

	Setting up the processes:
		There are two process-variables: 'media_process' and 'subtitle_process'. Each for one of the file types.
		There are actions, defined in the 'actions.py' file, that you can use to manipulate the files. The process
		variables are lists in which you will add entries of actions. That means that you will add a list of actions
		that will be executed on each file. An example of a subtitle process, in normal words:
			0) A subtitle file is added to the queue and send for processing
			1) Remove ads from the subtitle
			2) Make a .srt and .ass version of the subtitle if one of those doesn't exist already
			3) Update the plex library that the subtitle is in, so that plex notices the new file (created in step 2)

		-----

		A process entry looks like the following:
			{
				'action': action.example,
				'arguments': {
					'arg1': 'value1',
					'arg2': 'value2'
				}
			}
		The value of 'action' is one of the functions inside the 'actions.py' file that you want to run on the file.
		If you, for example, want to use the sub_remove_ads action inside your subtitle process, you add the following
		to your process:
			{
				'action': action.sub_remove_ads,
				'arguments': {}
			}
		The value of 'arguments' is just an empty dictionary because this action doesn't require arguments. The 'arguments'
		key is still required though, and if no arguments are required for the action, an empty dictionary is expected.
		Other actions might require additional arguments to be passed through. An example is the action sub_clone,
		which requires the desired extensions for the clones. To implement the sub_clone action into your process,
		you would add the following:
			{
				'action': action.sub_clone,
				'arguments': {
					'target_versions': ['srt','ass']
				}
			}
		The action sub_clone requires the argument 'target_versions' with the value of a list with extensions to make
		a clone for. You can see in the example above how to pass such argument to the action.

		You can find documentation about every action, how it manipulates the file and what argument(s) it needs (if any)
		inside the 'actions.py' file.

		-----

		The order of the actions can matter, though the actions are written in such way that the order shouldn't matter
		that much. See this example of a subtitle process:
			subtitle_process = [
				{
					'action': action.sub_clone,
					'arguments': {
						'target_versions': ['srt','ass']
					}
				},
				{
					'action': action.select_files,
					'arguments': {
						'target_files': ['srt','ass']
					}
				},
				{
					'action': action.sub_remove_ads,
					'arguments': {}
				}
			]
		This process will make a .srt and .ass version of the subtitle given, select all subtitles (why this select is here is
		explained later) and then remove ads in both subtitles. This would work as desired, as it achieves what we want:
		a .srt and .ass version of the subtitle without ads.

		However, when we turn the actions sub_remove_ads and sub_clone around and remove the select_files action, it will be more 
		efficient. The process shown above is inefficient because we first end up with two subtitles (from the sub_clone + 
		select_files) and then remove the ads from both subtitles. That means that we have to remove ads twice from identical 
		subtitles (identical except the container). When the two actions are switched around and the select_files is removed, 
		we remove ads from only one subtitle and then clone the ad-free subtitle to create two ad-free subtitles. This is more 
		efficient because we only need to remove ads once (instead of twice). Switching the actions around does require that you
		add 'replace': True to the arguments of the sub_clone action. This is because if the other version of the subtitle already
		exists, we need to replace it with the ad-free version of it instead of skipping it, so that we don't leave it as-is with
		the ads in it. We don't need the select_files anymore when we switch the actions around, which will be explained below.

		-----

		When setting up your process, you should take into account what the returned files will be. Take the following example:
			subtitle_process = [
				{
					'action': action.sub_clone,
					'arguments': {
						'target_versions': ['srt','ass']
					}
				},
				{
					'action': action.select_files,
					'arguments': {
						'target_files': ['srt','ass']
					}
				},
				{
					'action': action.sub_remove_ads,
					'arguments': {}
				}
			]
		The select_files action... selects files that will be processed from then on in the process. Imagine if the select_files
		wasn't there:
			0) A .srt file is processed; an .ass version already exists
			1) The file gets cloned to a .srt and .ass version
				- A .srt (original file) and .ass (mentioned at step 0) version already exists
				- Because all target versions already exist, no new files are made
				- Only newly added files are added to the selected list of files to be processed
				- The action only returns the starting .srt file because both version already exist (so no "new" files)
			2) The ads are removed from the file
				- The ads are only removed from the .srt file because that's the only file that is selected
				- The .ass is not processed
		We don't want this. We want to remove ads from both the .srt and the .ass file. There are three solutions to fix this:
			1: Switch the two actions around as said above so that the ads are removed from one file and then clones are made
			2: You add 'replace': True to the arguments of sub_clone. This will replace already existing versions instead of
			   skipping them. Replacing them counts as new files and thus they will be selected for the next actions.
			3: You add a select_files action in between. As an argument, you pass a list of files that you want to select on
			   top of the currently selected file. The files are matched starting from the back (so "select files
			   that end with 'ass' or 'srt' "). Now with all .srt and .ass files selected, we can move on to the sub_remove_ads 
			   action to remove the ads from all the selected subtitles.

		-----

		You can trust that the actions are smart. That means that every action detects if the files are subtitle or media files,
		the argument values are fool-proof processed and that multiple files are handled correctly. If you add a subtitle-specific
		action to the media_process, nothing should happen. The subtitle-action will just filter out all media files and only
		manipulate the subtitle files. The media files are returned without being touched so that the following action can use them
		(maybe the following action does manipulate the media files). That means that you can do the following, in normal words:
			0) A media file is added to the queue and send for processing
			1) Extract the subtitles from the media file (which results in an English and Italian external subtitle file)
			2) Remove ads from the subtitles (this subtitle-action will manipulate the extracted subtitle files; no need
			   for some sort of argument parsing, it. just. works.)
			2.5) A Spanish subtitle is added from external resources (e.g. Bazarr)
			3) Select the spanish subtitle to add it to the selected files in the process (or if step 2.5 is a seperate action,
			   the spanish subtitle will have been added there automatically)
			4) Transcode the media file to h265, adding the external subtitles back in (this media-action will manipulate both the
			   media file and the subtitles; no need to specifically select any files)
		You get it. It's a "flow" that should make it as easy and seamless as possible to manipulate files. No need to "select"
		anything unless it's for a specific reason; no need to specify the type of every file; no need to worry about subtitle-
		actions inside the media process and vice versa; no need to mess with the filepaths; no need to worry about file
		compatibility for certain actions (files are converted, processed and converted back automatically). It's still adviced
		though to have only one media file in your file list at the same time.

		-----

		Some actions require python packages to work. For example, the action sub_remove_ads requires the python packages 'chardet'
		and 'pysrt' in order to work. You need to install these in order to use this action. You can install packages the following
		way: 
			python3 -m pip install [package]
			#example
			python3 -m pip install chardet

To-Do:
	Actions
		Add/improve filters in media_transcode action
		Handle interruption of the script in media_transcode action (https://video.stackexchange.com/questions/32297/resuming-a-partially-completed-encode-with-ffmpeg)
		When action doesn't need to do anything, skip instead of executing empty command (media_transcode, media_extract_sub, sub_clone?)
		Filter argument to only apply action to filtered files for once
		New actions
			Rename audio tracks to their surround sound technology (e.g. Dolby Atmos or DTS X)
			Trigger bazarr "basic fixes" on subtitles
			Setting audio and subtitle stream for plex users
			Order streams in media files (v: res, a: channels -> lang, s: lang)
	Docs
		Add docs for creating your own action
		Setup wiki in GitHub
	General functioning
		Create proper plugin system
	V2
		Setup venv and auto install action-modules when needed
		API
		Allow adding folders to "monitor and convert"
		Sonarr/Radarr integration
			Interact with api to add connection
		Web-UI
			Websocket for queue, log, etc.
			index.html (top to bottom)
				system load
				current file processed
				log of file that is being processed
				queue
					File browser to add files to queue
			statistics.html (top to bottom)
				space saved
				history
			actions.html (top to bottom)
				visual rep of processes
				allow adding/removing/editing actions
				allow changing order
				display process in human words at the top in ordered list
				allow adding/removing/editing vars
		DB
			Store
				processes
				api key
				hosting settings
				statistics
				vars
"""

import os, logging
from time import sleep
from actions import action

#--------------------
#Settings
vars = {
	#ff locations
	'ffmpeg': './bin/ffmpeg',
	'ffprobe': './bin/ffprobe',

	#files
	'log_file': './Transcodarr.log',
	'queue_file': './Transcodarr.queue',
	'error_file': './Transcodarr.error',

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

vars = os.environ.get('Transcodarr_vars', vars)
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
