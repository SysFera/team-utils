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

To use `imdoing`, you need to add the following to your .bashrc (or similar):

    export TEAM_PATH=/PATH/TO/team-utils
    export PYTHONPATH=$PYTHONPATH:$TEAM_PATH/imdoing
    alias imdoing='python $TEAM_PATH/imdoing/imdoing.py'

To be able to use the time-tracking features, you need to use your own private API KEY instead of SysFera Bot's. To create/reset your API key, please go to https://support.sysfera.com/my/account in the left column. Then, add the following to your .bashrc (or similar):
    export CHILI_API_KEY=XXX


#### bash completion

(bash completion is currently not up-to-date. Please update it ;))

Copy the `imdoing` file to your /etc/bash_completion.d/ directory (it most likely requires superuser rights) to have bash completion of (most) imdoing commands.

### Commands

All commands can be invoked with the -h or --help parameter for more information.

Ex.: `imdoing -h`, `imdoing create -h`

#### mine

`imdoing mine` lists the tickets of USER. If no USER is supplied, the current user is used (see below for how the current user is found).

#### list

`imdoing list STATUS` lists the tickets that have the current sprint as their target and the specified STATUS. STATUS can be all, closed, open (default). The output is color-coded according to the tickets' statuses, as explained by a legend.


#### current

`current` is an alias for `list`.

#### create

`imdoing create` is used to create a new ticket and can take a number of options.

- -p/--parent PARENT: PARENT is the parent of the newly created subticket. If this option is not used, PROJECT must be specified (see below).
- -P/--project "PROJECT": "PROJECT" is the name of an existing project in which to create the new ticket. If this option is not used, PARENT must be specified (see above).
- -s/--subject: the ticket's subject. (required)
- -d/--description: the ticket's description. (required)
- -t/--tracker : the ticket's tracker. Can be bug, b, enhancement, e, support, s, team, t. (required)
- --priority: the priority for the ticket. Can be high, immediate, low, normal (default), urgent.
- --status: the status the ticket should be set to. Can be closed, new (default), open, rejected, solved.
- --assigned_to: the user to assign the ticket to. Can be a USER or "nobody" (default).
- --of: the OF for the ticket. Defaults to blank if PROJECT is used or to the PARENT's OF if PARENT is used.

#### update

`imdoing update TICKET#` is used to update one or several attributes of a ticket.

- --force/-f: a flag to force changing the assignee of a ticket (to prevent accidentally removing someone).
- --assigned_to/-a: the user to assign the ticket to. Can be a USER.
- --tracker/-t : the ticket's tracker. Can be bug, b, enhancement, e, support, s, team, t.
- --priority/-p: the priority for the ticket. Can be high, immediate, low, normal, urgent.
- --status/-s: the status the ticket should be set to. Can be closed, new, open, rejected, solved..
- --notes/-n: any additional comments to add to the ticket.

#### time

`imdoing time TICKET# USER` uses Time Entries in ChiliProject to clock in the time spent on a ticket. It takes a number of options:

- --hours (required): the number of hours spent on the ticket. Can be an integer or a float (US format: 4.2 and not 4,2).
- --date (optional): the day on which the hours were done. The format is "YYYY-MM-DD". Defaults to "today".
- --comments (optional): additional comments on the time spent ("Ran into a problem", "Was disturbed every other minute", etc.)

#### assign

`imdoing assign` is now deprecated. Please use `imdoing update` instead (see above).

#### status

`imdoing status` is now deprecated. Please use `imdoing update` instead (see above).

#### start / stop

NOTE: these actions are in the process of being replace by `imdoing time` (see above).

`imdoing ACTION TICKET# USER` registers that USER has started/stopped working on ticket TICKET# at the time the command was typed.
ACTION can be start or stop. If no USER is supplied, the current user is used (see below for how the current user is found).

For the registration, first, the timelog server is contacted. If it is not reachable, the timelog is saved as a file. If it is, the log is saved in a database. If there is an error, the timelog is saved as a file instead.

If the server was not unreachable, the program attempts to see if there are files (i.e., if some timelogs could previously not be saved). If there are, it attempts to save each of them. For each, if it suceeds, it removes the file. If it doesn't, it leaves the file for another time.

### Current user

To facilitate usage, there is a map in the config file that matches ChiliProject user ids to a "name". `imdoing` gets that name by doing the equivalent of a `whoami`. If you want to use `imdoing` and that your computer's username is different from your ChiliProject's username, you will need to edit the configuration file.

### Server

NOTE: the server will become outdated when the process of moving from `imdoing start/stop` to `imdoing time` is completed.

The server that `imdoing start/stop` tries to communicate with is contained in server.py. It is currently run on morgan-slave and accessible on morgan on port 9090 (http://192.168.1.2:9090).

#### /register

`/register` is the entry point for the `imdoing start/stop` script to register information. It should not be accessed in the browser.

#### /timelog/USER

`/timelog/USER` is a page that displays the current content of each user's timelog.

#### TODO

Post-processing needs to be implemented, in order to convert a list of start/stop action for a user and a ticket into a total duration spent by a user on a ticket.