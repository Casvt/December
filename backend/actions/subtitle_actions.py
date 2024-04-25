#-*- coding: utf-8 -*-

from dataclasses import dataclass
from os import remove
from os.path import isfile, splitext
from subprocess import Popen
from typing import Collection, Dict, List, Sequence, Union

from chardet import detect
from pysrt import open as srt_open

from backend.actions.general_actions import Action, ActionVars
from backend.config import Config


@dataclass
class SubCloneVars(ActionVars):
	target_versions: Sequence[str]
	"List of codecs that need to be made if they don't exist already"

	replace_existing: bool = False
	"Replace existing codecs with the clones made now"

	file_filter: Union[List[str], None] = None
	"Only process files that contain at least one of the strings in the list"

	def __post_init__(self) -> None:
		if not isinstance(self.target_versions, list):
			raise TypeError
		if not all(isinstance(v, str) for v in self.target_versions):
			raise TypeError
		self.target_versions = tuple(v.lstrip('.') for v in self.target_versions)
		if not all(2 <= len(v) <= 4 for v in self.target_versions):
			raise ValueError("Invalid codec supplied for SubClone action")

		if not isinstance(self.replace_existing, bool):
			raise TypeError

		if not (self.file_filter is None or isinstance(self.file_filter, list)):
			raise TypeError
		if self.file_filter is not None:
			if not all(isinstance(f, str) for f in self.file_filter):
				raise TypeError

		return


class SubClone(Action):
	"""
	Make multiple versions of a subtitle with different codecs. New files are
	only made if the codec doesn't already exist for the subtitle. Files, created
	or already existing, will be added to the list of files.

	E.g.
		srt -> srt + ass

		srt + ass -> srt + ass
	"""

	var_class = SubCloneVars

	def __init__(self, vars: SubCloneVars) -> None:
		self.vars = vars
		return

	def __create_clones(self, source_file: str, target_files: List[str]) -> None:
		proc = Popen(
			[
				self.config.ffmpeg, "-y",
				"-v", "quiet",
				"-i", source_file
			] + target_files
		)
		proc.wait()
		return

	def run(self, files: List[str]) -> List[str]:
		self.config = Config().config
		extra_files: List[str] = []

		if self.vars.file_filter is not None:
			sub_files = [
				file for file in files
				if file.endswith(self.config.subtitle_filter)
					and any(f in file for f in self.vars.file_filter)
			]
		else:
			sub_files = [
				file for file in files
				if file.endswith(self.config.subtitle_filter)
			]

		file_to_codec: Dict[str, List[str]] = {}
		for file in sub_files:
			st = splitext(file)
			file_to_codec.setdefault(st[0], []).append(st[1][1:])

		for sub, codecs in file_to_codec.items():
			missing_codecs = [tv for tv in self.vars.target_versions if not tv in codecs]
			new_files: List[str] = []
			for cod in missing_codecs:
				prop_filename = f"{sub}.{cod}"
				if not isfile(prop_filename):
					new_files.append(prop_filename)
				elif self.vars.replace_existing:
					remove(prop_filename)
					new_files.append(prop_filename)
				else:
					extra_files.append(prop_filename)

			if new_files:
				self.__create_clones(f"{sub}.{codecs[0]}", new_files)
				for f in new_files:
					self.config.logger.info(f"Created {f}")
				extra_files += new_files

		if not extra_files:
			self.config.logger.info("No sub clones made")
		else:
			files += extra_files
		return files


@dataclass
class SubRemoveAdsVars(ActionVars):
	extra_ads: Union[Collection[str], None] = None
	"""
	On top of the default list of ad texts, also remove lines if they contain one
	of the values in the list.
	"""

	file_filter: Union[List[str], None] = None
	"Only process files that contain at least one of the strings in the list"

	def __post_init__(self) -> None:
		if self.extra_ads is not None:
			if not isinstance(self.extra_ads, list):
				raise TypeError
			if not all(isinstance(v, str) for v in self.extra_ads):
				raise TypeError
			self.extra_ads = set(self.extra_ads)

		if self.file_filter is not None:
			if not isinstance(self.file_filter, list):
				raise TypeError
			if not all(isinstance(f, str) for f in self.file_filter):
				raise TypeError

		return


class SubRemoveAds(Action):
	"Remove advertisements (ads) from a subtitle"

	var_class = SubRemoveAdsVars

	def __init__(self, vars: SubRemoveAdsVars) -> None:
		self.vars = vars
		self.ads = {
			'created by', 'created and encoded by', 'corrected by', 'resync for', 'resyncimproved', 'ripped by', 'subtitles by', 'synchronized by', 'synccorrections by', 'sync and corrections by', 'sync by',
			'addic7ed', 'argenteam', 'allsubs',  'substeam', 'subscene', 'subdivx', 'synccorrected', 'tvsubtitles', 'tacho8',
			'nordvpn', 'a card shark americascardroom', 'advertise your product or brand here', 'everyone is intimidated by a shark. become', 'support us and become vip member',
			'opensubtitles', 'opensubtitles', 'open subtitles', 'mkv player', 'mkv player',
			'apóyanos y conviértete en miembro vip para', 'entre a americascardroom.com hoy', 'juegue poker en línea por dinero real', 'sigue "community" en', 'subtitulado por', 'subtitulamos', 'sincronizado y corregido por'
		}
		if self.vars.extra_ads:
			self.ads.union(self.vars.extra_ads)
		return

	def __create_version(self, source_file: str, target_file: str) -> None:
		proc = Popen(
			[
				self.config.ffmpeg, "-y",
				"-v", "quiet",
				"-i", source_file,
				target_file
			]
		)
		proc.wait()
		return

	def __remove_ads(self, file: str) -> bool:
		result_modified = False

		with open(file, 'rb') as f:
			encoding = detect(f.read())['encoding']
		if not encoding:
			encoding = 'utf-8'

		try:
			subs = srt_open(file, encoding=encoding)
			for i, line in enumerate(subs):
				if any(ad in line.text.lower() for ad in self.ads):
					del subs[i]
					result_modified = True
			subs.save(file)

		except UnicodeDecodeError:
			self.config.logger.error(f'Failed to decode subtitle for {file}')
			remove(file)

		except Exception as e:
			self.config.logger.exception(f'Failed to process subtitle for {file}')
			remove(file)

		return result_modified

	def run(self, files: List[str]) -> List[str]:
		self.config = Config().config

		if self.vars.file_filter is not None:
			sub_files = [
				file for file in files
				if file.endswith(self.config.subtitle_filter)
					and any(f in file for f in self.vars.file_filter)
			]
		else:
			sub_files = [
				file for file in files
				if file.endswith(self.config.subtitle_filter)
			]

		for file in sub_files:
			process_file = file

			if splitext(file)[1] != '.srt':
				# We can only edit srt files, so
				# convert to srt, process, then convert back
				process_file = splitext(file)[0] + '.ad_removal.srt'
				self.__create_version(file, process_file)

			if self.__remove_ads(process_file):
				self.config.logger.info(f'Removed ads from {file}')
			else:
				self.config.logger.info(f'No ads found in {file}')

			if process_file != file:
				# Convert converted file back
				remove(file)
				self.__create_version(process_file, file)
				remove(process_file)

		return files
