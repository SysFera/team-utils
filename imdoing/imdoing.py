#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

import os
import argparse
import json
import mine
import sys
import getpass
from redmine import Redmine
import current
import create
import assign
import status
import mytime


def parse_command_line():
    parser = argparse.ArgumentParser(
        description='Front to the imdoing commands.')
    parser.add_argument('command',
                        type=str,
                        help='the imdoing command to run',
                        choices=["mine", "current", "create",
                                 "assign", "status", "start", "stop"])
    parser.add_argument('arguments',
                        nargs=argparse.REMAINDER,
                        help='the command arguments')
    args = parser.parse_args()
    return args.command, args.arguments


def get_dir():
    directory = os.environ.get('TEAM_PATH')
    if directory is not None:
        return os.path.join(directory, "imdoing")
    print "The environment variable TEAM_PATH is not set. Aborting."
    sys.exit()


configFile = open(os.path.join(get_dir(), os.pardir,
                               'dashboard', 'data',
                               'config.json'))
config = json.load(configFile)
configFile.close()
URL = config['chili']['url']
API = config['chili']['api']
USERS = config['chili']['members']
USERNAMES = [str(U['name']) for U in USERS]
CUSTOMER_PROJECTS = config['chili']['customerProjects']
SYSFERA_PROJECTS = config['chili']['sysferaProjects']
TARGET_VERSION = config['sprint']['version_id']
TRACKERS = config['sprint']['trackers']
STATUSES = config['sprint']['statuses']
PRIORITIES = config['sprint']['priorities']


def main():
    user = getpass.getuser()

    rmine = Redmine(URL, key=API, requests={'verify': False})
    command, arguments = parse_command_line()
    if command == 'mine':
        mine.run(rmine, arguments, USERNAMES, USERS)
    elif command == 'current':
        current.run(rmine, TARGET_VERSION, USERS)
    elif command == 'create':
        create.run(rmine, arguments, TARGET_VERSION, user, TRACKERS, PRIORITIES)
    elif command == 'assign':
        assign.run(rmine, arguments, USERS, USERNAMES)
    elif command == 'status':
        status.run(rmine, arguments, STATUSES)
    elif command == 'start':
        mytime.run(arguments, get_dir(), "start", USERNAMES)
    elif command == 'stop':
        mytime.run(arguments, get_dir(), "stop", USERNAMES)
    sys.exit()


if __name__ == '__main__':
    main()
