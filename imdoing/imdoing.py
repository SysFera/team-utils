#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

import os
import argparse
import subprocess
import json
import mine
import sys
from redmine import Redmine
import target
import create
import assign
import mytime


def parse_command_line():
    parser = argparse.ArgumentParser(
        description='Front to the imdoing commands.')
    parser.add_argument('command',
                        type=str,
                        help='the imdoing command to run',
                        choices=["mine", "current", "create",
                                 "assign", "start", "stop"])
    parser.add_argument('arguments',
                        nargs=argparse.REMAINDER,
                        help='the command arguments')
    args = parser.parse_args()
    command = args.command
    arguments = " ".join(args.arguments)
    return command, arguments


def get_dir():
    directory = os.environ.get('TEAM_PATH')

    if directory is not None:
        return os.path.join(directory, "imdoing")
    else:
        print "The environment variable TEAM_PATH is not set. Aborting."
        sys.exit()

# non-standard modules required
# pip install python-redmine
# pip install python-dateutil

configFile = open(os.path.join(get_dir(), 'config.json'))
config = json.load(configFile)
configFile.close()
URL = config['chili']['url']
API = config['chili']['api']
USERS = config['chili']['members']
USERNAMES = [str(U['name']) for U in USERS]
CUSTOMER_PROJECTS = config['chili']['customerProjects']
SYSFERA_PROJECTS = config['chili']['sysferaProjects']
SPRINT_TARGET = "%02d" % config['sprint']['end']['day'] + \
                "-" + "%02d" % config['sprint']['end']['month'] + \
                "-" + "%04d" % config['sprint']['end']['year']
TARGET_VERSION = config['sprint']['version_id']


def main():
    rmine = Redmine(URL, key=API, requests={'verify': False})
    command, arguments = parse_command_line()
    if command == 'mine':
        mine.run(rmine, arguments, USERNAMES, USERS)
    elif command == 'current':
        target.run(rmine, arguments, SPRINT_TARGET)
    elif command == 'create':
        create.run(rmine, arguments, USERS, TARGET_VERSION)
    elif command == 'assign':
        assign.run(rmine, arguments, USERS, USERNAMES)
    elif command == 'start':
        mytime.run(arguments, USERS, get_dir(), "start", USERNAMES)
    elif command == 'stop':
        mytime.run(arguments, USERS, get_dir(), "stop", USERNAMES)
    else : 
        print "Usage: imdoing <action>{create/assign/mine/current/start/stop} [options]"

    sys.exit()


if __name__ == '__main__':
    main()
