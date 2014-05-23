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

To use `imdoing`, you need to add the following to your .bashrc.

    export TEAM_PATH=/path/to/team-utils
    export PATH=$PATH:$TEAM_PATH/imdoing
    alias imdoing='imdoing.py'

Add the `imdoing` file to your /etc/bash_completion.d/ directory to have the bash completion

### Commands

All commands can be invoked with the -h or --help parameter for more information.

Ex.: `imdoing -h`, `imdoing create -h`

#### mine

`imdoing mine` lists the tickets of USER. If no USER is supplied, the current user is used (see below for how the current user is found).

#### current

`imdoing current` lists the tickets that have the current sprint as their target.

#### create

`imdoing create -p PARENT# -s SUBJECT -d DESCRIPTION -t TYPE` creates a new ticket child of PARENT# with SUBJECT and DESCRIPTION, of TYPE (which can be "bug", "enhancement", "support", "team").

This simply creates the ticket but does not assign it to anyone.

#### assign

`imdoing assign TICKET# USER` assigns TICKET# to USER and sets its status to "Open". If no USER is supplied, the current user is used (see below for how the current user is found).

#### start / stop

`imdoing ACTION TICKET# USER` creates a file in the TEAM_PATH/imdoing/USER directory with the TIME, TICKET#, ACTION and USER in its name.

ACTION can be start or stop. If no USER is supplied, the current user is used (see below for how the current user is found).

### Current user

To facilitate usage, there is a map in the config file that matches ChiliPorject user ids to a "name". `imdoing` gets that name by doing the equivalent of a `whoami`. If you want to use `imdoing` and that your computer's username is different from your ChiliProject's username, you will need to edit the configuration file.