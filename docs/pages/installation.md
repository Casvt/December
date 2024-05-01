# Installation

## Installation

=== "Linux"
	```bash
	sudo apt-get install git python3-pip
	sudo git clone https://github.com/Casvt/December.git /opt/December
	cd /opt/December
	python3 -m pip install -r requirements.txt
	```
	
	Now set up your [config file](./config.md). Once you've done that, use the following command to run December (replace `/path/to/config.json` with the correct path).

	```bash
	python3 December.py -c "/path/to/config.json"
	```

=== "Windows"
    On Windows, there are a couple of extra steps involved.  

    1. [Download and instal Python](https://www.python.org/downloads/). This is the framework MIND runs on top of.  
       _Make sure you select to add Python to PATH when prompted. This will make installing requirements much easier._
    2. Download (or clone) the [latest December release](https://github.com/Casvt/December/releases/latest).  
    3. Extract the zip file to a folder on your machine.  
       We suggest something straightforward - `C:\apps\December` is what we'll use as an example.
    4. Instal the required python modules (found in `requirements.txt`).
       This can be done from a command prompt, by changing to the folder you've extracted December to and running a python command.
		```powershell
		cd C:\apps\December
		python -m pip install -r requirements.txt
		```

	Now set up your [config file](./config.md). Once you've done that, use the following command to run December (replace `C:\path\to\config.json` with the correct path).

	```powershell
	python December.py -c "C:\path\to\config.json"
	```

## Usage

Once December is running, you can start transcoding files. Add filepaths to the queue file one by one and December will handle them. You can also make Radarr and/or Sonarr automatically add the filepath of a newly downloaded file to the queue file.

To set that up, first create a new file that will run the command.

=== "Linux"
	1. Create a bash file, e.g. `/opt/December/connect.sh`.
	2. Give it the following content, and replace the paths with the correct values.
	```bash
	#!/bin/bash

	cd /opt/December
	python3 December.py -c /path/to/config.json
	```

=== "Windows"
	1. Create a bat file, e.g. `C:\apps\December\connect.bat`
	2. Give it the following content, and replace the paths with the correct values.
	```bat
	python "C:\apps\December\December.py" -c "C:\path\to\config.json"
	```

Now setup Radarr/Sonarr to run the script.

1. In either Radarr or Sonarr, go to Settings -> Connect -> `+` -> Custom Script.
2. Select "On Import" and "On Upgrade".
3. For the "Path", give the path to the script that we just created. E.g. `/opt/December/connect.sh`.
4. Click "Save".
