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
import update
import mytime


def parse_command_line():
    parser = argparse.ArgumentParser(
        description='Front to the imdoing commands.')
    parser.add_argument('command',
                        type=str,
                        help='the imdoing command to run',
                        choices=["mine", "list", "current", "create", "update",
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


TEAM_PATH = get_dir()
configFile = open(os.path.join(TEAM_PATH, os.pardir,
                               'dashboard', 'data',
                               'config.json'))
config = json.load(configFile)
configFile.close()
REGISTER_URL = config['global']['register_url']
URL = config['chili']['url']
API = config['chili']['api']
USERS = config['chili']['members']
USERNAMES = [str(U['name']) for U in USERS]
CUSTOMER_PROJECTS = config['chili']['customerProjects']
SYSFERA_PROJECTS = config['chili']['sysferaProjects']
TARGET_VERSION = config['chili']['version_id']
TRACKERS = config['chili']['trackers']
STATUSES = config['chili']['statuses']
PRIORITIES = config['chili']['priorities']


def dispatch(command, arguments):
    rmine = Redmine(URL, key=API, requests={'verify': False})
    if command == 'mine':
        mine.run(rmine, arguments, USERNAMES, USERS)
    elif command == 'current':
        current.run(rmine, TARGET_VERSION, USERS)
    elif command == 'list':
        current.run(rmine, TARGET_VERSION, USERS)
    elif command == 'create':
        create.run(rmine, arguments, TARGET_VERSION, USERS, TRACKERS,
                   PRIORITIES, CUSTOMER_PROJECTS+SYSFERA_PROJECTS, STATUSES)
    elif command == 'assign':
        assign.run(arguments, USERNAMES)
    elif command == 'status':
        status.run(arguments, STATUSES)
    elif command == 'update':
        update.run(rmine, arguments, USERS, STATUSES, PRIORITIES, TRACKERS)
    elif command == 'start':
        mytime.run(arguments, TEAM_PATH, "start", USERS, STATUSES,
                   REGISTER_URL)
    elif command == 'stop':
        mytime.run(arguments, TEAM_PATH, "stop", USERS, STATUSES,
                   REGISTER_URL)
    sys.exit()


def main():
    c, a = parse_command_line()
    dispatch(c, a)


if __name__ == '__main__':
    main()
