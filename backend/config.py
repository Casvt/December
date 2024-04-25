#-*- coding: utf-8 -*-

from dataclasses import dataclass, field
from importlib import import_module
from json import JSONDecodeError, load
from logging import Logger, _nameToLevel
from os import sep, walk
from os.path import abspath, isfile, join, splitext
from typing import Any, Dict, Mapping, Sequence, Tuple, Type, Union

from requests import get
from requests.exceptions import RequestException

from backend.actions.general_actions import Action, ActionEntry
from backend.helpers import Singleton, T
from backend.logging import setup_logging


@dataclass
class ConfigValues:
	logging_level: int
	logger: Logger

	ffmpeg: str
	ffprobe: str

	log_file: str
	queue_file: str
	error_file: str

	check_interval: int = 30

	media_filter: Tuple[str, ...] = field(default_factory=lambda: ('.mkv','.mp4','.mov','.m4v','.mpg','.mpeg','.avi','.flv','.webm'))
	subtitle_filter: Tuple[str, ...] = field(default_factory=lambda: ('.srt', '.ass'))

	plex_setup: bool = False
	plex_base_url: Union[str, None] = None
	plex_api_token: Union[str, None] = None

	sonarr_setup: bool = False
	sonarr_base_url: Union[str, None] = None
	sonarr_api_token: Union[str, None] = None

	radarr_setup: bool = False
	radarr_base_url: Union[str, None] = None
	radarr_api_token: Union[str, None] = None

	media_process: Sequence[Action] = field(default_factory=lambda: [])
	subtitle_process: Sequence[Action] = field(default_factory=lambda: [])


class Config(metaclass=Singleton):
	"Note: is singleton"
	
	def __init__(self, config_file: str = '') -> None:
		self.file = config_file

		for current, folders, files in walk(join('backend', 'actions')):
			if '__pycache__' in current:
				continue
			base_path = '.'.join(current.split(sep))
			for f in files:
				st = splitext(f)
				if st[1] == '.py' and f[0] != '__init__':
					import_module('.'.join((base_path, st[0])))

		self.str_to_action: Dict[str, Type[Action]] = {
			c.__module__.split('actions.')[-1] + '.' + c.__name__: c
			for c in Action.__subclasses__()
		}

		self.reload_config()
		return

	def reload_config(self) -> None:
		from backend.logging import LOGGER

		if not self.file:
			raise ValueError("Config file needs to be given")
		if not isfile(self.file):
			raise ValueError("Config file does not exist")
		try:
			with open(self.file, 'r') as f:

				contents = load(f)
				if not isinstance(contents, dict):
					raise ValueError("Config file contains unsupported JSON; expected an object")

				result = self.__parse_config(contents)
				setup_logging(result['log_file'], result['logging_level'])
				self.config = ConfigValues(**{
					**result,
					"logger": LOGGER
				})
				self.config.logger.info(f'Set config: {self.config}')

		except (OSError, IOError, PermissionError):
			raise ValueError("Failed to open config file")
		except JSONDecodeError:
			raise ValueError("Config file contains invalid JSON")

		return

	def __parse_config(self, config: Mapping[str, Any]) -> Dict[str, Any]:
		final_config = {}
		value: Any

		def get_required_value(key: str, check_type: Type[T], check_truthy: bool) -> T:
			value = config.get(key)
			if value is None:
				raise ValueError(f"Required setting not found in config file: {key}")
			if not isinstance(value, check_type):
				raise ValueError(f"Invalid value for setting in config file: {key}")
			if check_truthy:
				if not value:
					raise ValueError(f"Invalid value for setting in config file: {key}")
			return value

		def get_optional_key(key: str, default: T, check_type: Type[T]) -> T:
			value = config.get(key)
			if value is None:
				value = default
			if not isinstance(value, check_type):
				raise ValueError(f"Invalid value for setting in config file: {key}")
			return value

		logging_level = get_required_value('logging_level', str, True)
		if not logging_level in ('info', 'debug'):
			raise ValueError("Invalid value for setting in config file: 'logging_level'")
		final_config['logging_level'] = _nameToLevel[logging_level.upper()]

		for key in ('ffmpeg', 'ffprobe'):
			value = abspath(get_required_value(key, str, True))
			if not isfile(value):
				raise ValueError(f"Executable not found for setting in config file: {key}")
			final_config[key] = value

		for key in ('log_file', 'queue_file', 'error_file'):
			value = abspath(get_required_value(key, str, True))
			if not isfile(value):
				try:
					open(value, "a")
				except (OSError, IOError, PermissionError):
					raise ValueError(f"Failed to create file for setting in config file: {key}")
			final_config[key] = value

		check_interval = get_optional_key('check_interval', 30, int)
		if not check_interval > 0:
			raise ValueError(f"Invalid value for setting in config file: 'check_interval'")
		final_config['check_interval'] = check_interval

		media_filter = tuple(get_optional_key(
			'media_filter',
			['.mkv','.mp4','.mov','.m4v','.mpg','.mpeg','.avi','.flv','.webm'],
			list
		))
		for f in media_filter:
			if not isinstance(f, str) or not f or f[0] != '.' or not 3 <= len(f) <= 5:
				raise ValueError(f"Invalid value for setting in config file: 'media_filter'")
		final_config['media_filter'] = media_filter

		subtitle_filter = tuple(get_optional_key(
			'subtitle_filter',
			['.srt', '.ass'],
			list
		))
		for f in subtitle_filter:
			if not isinstance(f, str) or not f or f[0] != '.' or not 3 <= len(f) <= 4:
				raise ValueError(f"Invalid value for setting in config file: 'subtitle_filter'")
		final_config['subtitle_filter'] = subtitle_filter

		plex_base_url = get_optional_key(
			'plex_base_url',
			'',
			str
		)
		plex_api_token = get_optional_key(
			'plex_api_token',
			'',
			str
		)
		if plex_base_url and plex_api_token:
			try:
				success = get(f'{plex_base_url}/', params={'X-Plex-Token': plex_api_token}).ok
			except RequestException:
				success = False
			if not success:
				raise ValueError(f"Can't connect to plex with given values")
			final_config['plex_setup'] = True
			final_config['plex_base_url'] = plex_base_url
			final_config['plex_api_token'] = plex_api_token

		sonarr_base_url = get_optional_key(
			'sonarr_base_url',
			'',
			str
		)
		sonarr_api_token = get_optional_key(
			'sonarr_api_token',
			'',
			str
		)
		if sonarr_base_url and sonarr_api_token:
			try:
				success = get(f'{sonarr_base_url}/api/v3/system/status', params={'apikey': sonarr_api_token}).ok
			except RequestException:
				success = False
			if not success:
				raise ValueError(f"Can't connect to sonarr with given values")
			final_config['sonarr_setup'] = True
			final_config['sonarr_base_url'] = sonarr_base_url
			final_config['sonarr_api_token'] = sonarr_api_token

		radarr_base_url = get_optional_key(
			'radarr_base_url',
			'',
			str
		)
		radarr_api_token = get_optional_key(
			'radarr_api_token',
			'',
			str
		)
		if radarr_base_url and radarr_api_token:
			try:
				success = get(f'{radarr_base_url}/api/v3/system/status', params={'apikey': radarr_api_token}).ok
			except RequestException:
				success = False
			if not success:
				raise ValueError(f"Can't connect to radarr with given values")
			final_config['radarr_setup'] = True
			final_config['radarr_base_url'] = radarr_base_url
			final_config['radarr_api_token'] = radarr_api_token

		media_process = get_optional_key(
			'media_process',
			[],
			list
		)
		media_result = []
		final_config['media_process'] = media_result
		for p in media_process:
			try:
				if not isinstance(p, dict):
					raise ValueError(f"Invalid value for setting in config file: 'media_process'")

				action_entry = ActionEntry(**p)
				action_class = self.str_to_action.get(action_entry.action)
				if action_class is None:
					raise ValueError(f"Unknown action: {action_entry.action}")
				action_vars = action_entry.vars
				action_vars_class = action_class.var_class

				if action_vars_class is None:
					inst = action_class(None)
				else:
					inst = action_class(action_vars_class(**action_vars))

				media_result.append(inst)

			except TypeError:
				raise ValueError(f"Invalid value for setting in config file: 'media_process' -> {p}")

		subtitle_process = get_optional_key(
			'subtitle_process',
			[],
			list
		)
		subtitle_result = []
		final_config['subtitle_process'] = subtitle_result
		for p in subtitle_process:
			if not isinstance(p, dict):
				raise ValueError(f"Invalid value for setting in config file: 'subtitle_process'")

			try:
				if not isinstance(p, dict):
					raise ValueError(f"Invalid value for setting in config file: 'subtitle_process'")

				action_entry = ActionEntry(**p)
				action_class = self.str_to_action.get(action_entry.action)
				if action_class is None:
					raise TypeError
				action_vars = action_entry.vars
				action_vars_class = action_class.var_class

				if action_vars_class is None:
					inst = action_class(None)
				else:
					inst = action_class(action_vars_class(**action_vars))

				subtitle_result.append(inst)

			except TypeError:
				raise ValueError(f"Invalid value for setting in config file: 'subtitle_process' -> {p}")

		return final_config
