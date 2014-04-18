#!/bin/bash
############################
# sync.sh
# This script merges a number of config_ files to create a working .ssh/config file.
# Any custom file named config_* will be included in the merge, in alphanumerical order.
# /!\ No conflict detection, be careful and check the final file manually. /!\
############################

########## Variables
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
now=$(date +"%Y-%m-%d_%H:%M")
repo=$SCRIPT_PATH               # repository directory
home=~
gitbak=$repo/git_$now             # backup directory


echo "Making a backup of .gitmessage to $gitbak..."
mkdir -p $gitbak
mv $home/.gitmessage $gitbak
echo "Done."
echo "==="

echo "Creating the symbolic link"
ln -s $repo/git/.gitmessage $home/.gitmessage
echo "Done."
echo "Remember that a backup of your previous .gitmessage was made in $gitbak."
echo 
echo "Tell git to use the .gitmessage using the following:"
echo "    git config --global commit.template $home/.gitmessage"
echo ""
