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
ssh=~/.ssh                       # .ssh directory
repo=$SCRIPT_PATH               # repository directory
dir=$repo/ssh                    # ssh directory
sshbak=$repo/ssh_$now             # backup directory

##########
# change to the ssh directory
echo -n "Changing to the $ssh directory..."
if [ ! -d $ssh ]; then
  mkdir -p $ssh
fi
pushd $ssh > /dev/null
echo "Done."

echo "Making a backup of $ssh to $sshbak..."
mkdir -p $sshbak
cp -R $ssh/* $sshbak
echo "Done."

echo "==="
echo "Creating the new $ssh/config..."
cd $dir/conf
echo "Adding the configuration files..."
echo "Tip: you can add custom rules in the configPersonal file."
echo "# Careful: do not edit this file directly; it is generated and your changes will be erased!" > config
echo "# Edit/create configPersonal or configSOMETHING instead" >> config
for file in `ls config?*`; do
  if ! [[ $file =~ .*\..* ]]; then
    cat $file >> config
    echo "" >> config
    echo "" >> config
  fi
done
echo "Done."
echo "Moving the new config file to $ssh"
mv $repo/ssh/conf/config $ssh/config
echo "Done creating $ssh/config."

echo "==="

echo "Copying the keys..."
echo "cd $dir/keys"
cd $dir/keys
rm -rf $ssh/customerKeys > /dev/null
mkdir -p $ssh/customerKeys
cp * $ssh/customerKeys
chmod 600 $ssh/customerKeys/*
echo "Done."
echo "==="
popd > /dev/null
echo "Finished."
echo "Remember that a backup of your previous $ssh was made in $sshbak."