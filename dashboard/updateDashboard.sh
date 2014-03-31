#!/bin/bash

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Last update at `date`" > /tmp/teamutils.log
cd $SCRIPT_PATH
git pull

