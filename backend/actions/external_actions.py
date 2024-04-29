#-*- coding: utf-8 -*-

from os.path import dirname
from typing import Any, Dict, List

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
				# Folder has already been scanned.
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
			self.config.logger.info("File(s) not found in Plex")

		return files


class BazarrCommonFixes(Action):
	"""
	Trigger the Bazarr "Common Fixes" for the subtitles.
	"""

	var_class = None

	def __init__(self, vars: None) -> None:
		self.vars = vars
		return

	def run(self, files: List[str]) -> List[str]:
		self.config = Config().config

		if not self.config.bazarr_setup:
			raise ValueError("Bazarr variables need to be set up in order to use BazarrCommonFixes")

		ssn = Session()
		ssn.headers.update({"Accept": "application/json"})
		ssn.params.update({"apikey": self.config.bazarr_api_token}) # type: ignore

		sub_files = [
			file for file in files
			if file.endswith(self.config.subtitle_filter)
		]

		movies: Dict[str, Dict[str, Any]] = {
			dirname(m["path"]): m
			for m in ssn.get(
				f"{self.config.bazarr_base_url}/api/movies",
				params={"start": 0, "length": -1}
			).json()["data"]
		}
		series: Dict[str, Dict[str, Any]] = {
			s["path"]: s
			for s in ssn.get(
				f"{self.config.bazarr_base_url}/api/series",
				params={"start": 0, "length": -1}
			).json()["data"]
		}

		path_to_movie: Dict[str, Dict[str, Any]] = {}
		show_ids: List[int] = []
		for sub in sub_files:
			for path, movie in movies.items():
				if not sub.startswith(path):
					continue
				ssn.patch(
					f"{self.config.bazarr_base_url}/api/movies",
					files={"action": (None, "scan-disk"), "radarrid": (None, movie["radarrId"])}
				)
				path_to_movie[sub] = movie
				break
			else:

				for path, show in series.items():
					if not sub.startswith(path):
						continue
					ssn.patch(
						f"{self.config.bazarr_base_url}/api/series",
						files={"action": (None, "scan-disk"), "seriesid": (None, show["sonarrSeriesId"])}
					)
					show_ids.append(show["sonarrSeriesId"])
					break

		for sub, movie in path_to_movie.items():
			for m_sub in movie["subtitles"]:
				if not m_sub["path"] == sub:
					continue
				ssn.patch(
					f"{self.config.bazarr_base_url}/api/subtitles",
					params={"action": "common"},
					files={
						"id": (None, movie["radarrId"]),
						"type": (None, "movie"),
						"language": (None, m_sub["code2"]),
						"path": (None, sub)
					}
				)

		if not show_ids:
			return files

		ep_files = set((f for f in sub_files if not f in path_to_movie))
		url = f"{self.config.bazarr_base_url}/api/episodes?" + "&".join(
			(f"seriesid[]={i}" for i in show_ids)
		)
		episodes = ssn.get(url).json()["data"]

		for ep in episodes:
			for sub in ep["subtitles"]:
				if not sub["path"] in ep_files:
					continue
				ssn.patch(
					f"{self.config.bazarr_base_url}/api/subtitles",
					params={"action": "common"},
					files={
						"id": (None, ep["sonarrEpisodeId"]),
						"type": (None, "episode"),
						"language": (None, sub["code2"]),
						"path": (None, sub["path"])
					}
				)

		return files
