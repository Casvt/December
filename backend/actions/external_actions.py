#-*- coding: utf-8 -*-

from os.path import dirname
from typing import Dict, List

from requests import RequestException, Session

from backend.actions.general_actions import Action
from backend.config import Config


class PlexScan(Action):
	"""
	Trigger a scan in Plex for the media. It only does a partial scan,
	so Plex only updates the folder that the file is in, not a complete
	scan of the whole library. That means that this is very effecient and
	loads of files will not hurt the performance.
	"""

	var_class = None

	def __init__(self, vars: None) -> None:
		self.vars = vars
		return

	def run(self, files: List[str]) -> List[str]:
		self.config = Config().config

		if not self.config.plex_setup:
			raise ValueError("Plex variables need to be set up in order to use PlexScan")

		ssn = Session()
		ssn.headers.update({"Accept": "application/json"})
		ssn.params.update({"X-Plex-Token": self.config.plex_api_token}) # type: ignore

		try:
			r = ssn.get(
				f"{self.config.plex_base_url}/library/sections"
			)
			if not r.ok:
				raise RequestException
			libs: List[Dict[str, List[Dict[str, str]]]] = r.json()["MediaContainer"].get("Directory", [])
		except RequestException:
			self.config.logger.warning("Plex not reachable")
			return files

		paths = []
		for file in files:
			filepath = dirname(file)
			if filepath in paths:
				# Folder has not been scanned yet.
				# Avoids doing a scan for the same folder multiple times
				# because multiple files (e.g. media + subs) are handled.
				continue

			for lib in libs:
				for lib_folder in lib.get('Location', []):
					if filepath.startswith(lib_folder['path']):
						# File is in lib
						ssn.get(
							f"{self.config.plex_base_url}/library/sections/{lib['key']}/refresh",
							params={"path": filepath}
						)
						paths.append(filepath)
						break

		if paths:
			self.config.logger.info("Updated Plex library")
		else:
			self.config.logger.info("File not found in Plex")

		return files
