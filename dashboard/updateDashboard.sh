#!/bin/bash

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_PATH
git pull

# Python scripts
cd data
python chiliTeam.py
python chiliProjects.py
python jenkinsBuilds.py
python githubChangelogs.py
cd -