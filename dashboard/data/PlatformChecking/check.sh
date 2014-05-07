#!/bin/bash
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $SCRIPT_PATH
for i in `cat check.lst`;do 
	echo $i
	bash check${i}.sh
done
bash postCheck.sh
