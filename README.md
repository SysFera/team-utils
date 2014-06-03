# team-utils

Collection of internal tools for the SysFera technical team

## ssh

TODO

## git

TODO

## dashboard

TODO

## imdoing

"imdoing" is a utility to ease up timetracking and interaction with the ChiliProject.

### Prerequisites

#### Python

Some specific python modules are required to use imdoing: `python-redmine` et `python-dateutil` and can be installed using the pip package manager.

    pip install python-redmine
    pip install python-dateutil

Use these commands as root for a global installation.

If you need to install pip:

for Debian-based distros (as root):

    apt-get install python-pip

for OpenSuse (as root):

    zypper install python-pip


#### .bashrc

To use `imdoing`, you need to add the following to your .bashrc.

    export TEAM_PATH=/PATH/TO/team-utils
    export PYTHONPATH=$PYTHONPATH:$TEAM_PATH/imdoing
    alias imdoing='python $TEAM_PATH/imdoing/imdoing.py'


#### bash completion

Copy the `imdoing` file to your /etc/bash_completion.d/ directory (it most likely requires superuser rights) to have bash completion of (most) imdoing commands.

### Commands

All commands can be invoked with the -h or --help parameter for more information.

Ex.: `imdoing -h`, `imdoing create -h`

#### mine

`imdoing mine` lists the tickets of USER. If no USER is supplied, the current user is used (see below for how the current user is found).

#### current

`imdoing current` lists the tickets that have the current sprint as their target.

#### create

`imdoing create` is used to create a new ticket and can take a number of options.

- -p/--parent PARENT: PARENT is the parent of the newly created subticket. If this option is not used, PROJECT must be specified (see below).
- -P/--project "PROJECT": "PROJECT" is the name of an existing project in which to create the new ticket. If this option is not used, PARENT must be specified (see above).
- -s/--subject: the ticket's subject. (required)
- -d/--description: the ticket's description. (required)
- -t/--type : the ticket's type. Can be support, team, bug, enhancement. (required)
- --priority: the priority for the ticket. Can be low, normal (default), high, urgent, immediate.
- --of: the OF for the ticket. Defaults to blank if PROJECT is used or to the PARENT's OF if PARENT is used.

The ticket is created unassigned and with status set to "New".

#### assign

`imdoing assign TICKET# USER` assigns TICKET# to USER. If no USER is supplied, the current user is used (see below for how the current user is found).

USER can be "nobody", which will deassign the ticket. If the ticket is already assigned, there will be a warning message. To override it, the command needs to be run with the -f flag.

#### status

`imdoing status TICKET# STATUS` will change the status of ticket TICKET# to STATUS, which can be new, open, rejected, closed, solved.

#### start / stop

`imdoing ACTION TICKET# USER` registers that USER has started/stopped working on ticket TICKET# at the time the command was typed.
ACTION can be start or stop. If no USER is supplied, the current user is used (see below for how the current user is found).

For the registration, first, the timelog server is contacted. If it is not reachable, the timelog is saved as a file. If it is, the log is saved in a database. If there is an error, the timelog is saved as a file instead.

If the server was not unreachable, the program attempts to see if there are files (i.e., if some timelogs could previously not be saved). If there are, it attempts to save each of them. For each, if it suceeds, it removes the file. If it doesn't, it leaves the file for another time.

### Current user

To facilitate usage, there is a map in the config file that matches ChiliProject user ids to a "name". `imdoing` gets that name by doing the equivalent of a `whoami`. If you want to use `imdoing` and that your computer's username is different from your ChiliProject's username, you will need to edit the configuration file.