# Config

In the config file is specified what the process is and all the accompanying needed settings. It's in the JSON format.

## Setting up a config file.

First make the file, with a name like `December.config.json`. Paste the following into it:

```json
{
	"logging_level": "info",

	"ffmpeg": "./bin/ffmpeg",
	"ffprobe": "./bin/ffprobe",

	"log_file": "./December.log",
	"queue_file": "./December.queue",
	"error_file": "./December.error",

	"check_interval": 30,

	"plex_base_url": "",
	"plex_api_token": "",

	"sonarr_base_url": "",
	"sonarr_api_token": "",

	"radarr_base_url": "",
	"radarr_api_token": "",

	"bazarr_base_url": "",
	"bazarr_api_token": "",

	"media_process": [

	],

	"subtitle_process": [

	]
}
```

If you're running on Windows, you have to do two things:

1. Replace the `/` with `\` in the file.
2. Download FFMPEG and FFPROBE, then supply the paths to the executables to the `ffmpeg` and `ffprobe` setting respectively.

If possible, supply values for as many of the services as possible, as it enables access to more actions.

The values for `media_process` and `subtitle_process` describe the processes for the files. Each action is an object with the `action` key giving the identifier of the action and the `vars` key giving an object with action-specific settings. See an example below:

```json
{
	"logging_level": "info",

	"ffmpeg": "./bin/ffmpeg",
	"ffprobe": "./bin/ffprobe",

	"log_file": "./December.log",
	"queue_file": "./December.queue",
	"error_file": "./December.error",

	"check_interval": 5,

	"plex_base_url": "http://192.168.2.15:32400",
	"plex_api_token": "abcdefghijk",

	"sonarr_base_url": "http://192.168.2.15:8005",
	"sonarr_api_token": "abcdefghijk",

	"radarr_base_url": "http://192.168.2.15:8006",
	"radarr_api_token": "abcdefghijk",

	"bazarr_base_url": "http://192.168.2.15:8009",
	"bazarr_api_token": "abcdefghijk",

	"media_process": [
		{
			"action": "media_actions.MediaExtractSubs",
			"vars": {
				"codec": "srt",
				"language_tag": true,
				"extract_unknown_language": true,
				"remove_from_media": false,
				"extract_languages": ["en", "nl"],
				"extract_codecs": ["subrip"],
				"exclude_versions": ["sdh", "forced"]
			}
		},
		{
			"action": "subtitle_actions.SubRemoveAds",
			"vars": {}
		},
		{
			"action": "subtitle_actions.SubClone",
			"vars": {
				"target_versions": ["ass", "srt"],
				"replace_existing": true
			}
		},
		{
			"action": "media_actions.MediaTranscode",
			"vars": {
				"video": {
					"keep_video": true,
					"codec": "hevc_nvenc",
					"force_transcode": false,
					"preset": "p7"
				},
				"audio": {
					"keep_audio": true,
					"codec": "libfdk_aac",
					"force_transcode": false,
					"keep_unknowns": true,
					"keep_commentary": false,
					"keep_languages": ["en"],
					"keep_original_language": true,
					"keep_duplicates": false,
					"on_no_matches": "avoid_commentary",
					"create_channels": ["2.0"]
				},
				"subtitle": {
					"keep_subtitle": false,
					"keep_unknowns": true
				},
				"general": {
					"keep_metadata": false,
					"keep_poster": false
				}
			}
		},
		{
			"action": "external_actions.BazarrCommonFixes",
			"vars": {}
		},
		{
			"action": "external_actions.PlexScan",
			"vars": {}
		}
	],

	"subtitle_process": [
		{
			"action": "subtitle_actions.SubRemoveAds",
			"vars": {}
		},
		{
			"action": "subtitle_actions.SubClone",
			"vars": {
				"target_versions": ["ass", "srt"],
				"replace_existing": true
			}
		},
		{
			"action": "external_actions.BazarrCommonFixes",
			"vars": {}
		},
		{
			"action": "external_actions.PlexScan",
			"vars": {}
		}
	]
}
```
