#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

from redmine import Redmine
import os
import argparse
import json
import mine
import sys
import current
import create
import assign
import status
import timesheet
import export
import update
import mytime
import timelog


def parse_command_line():
    parser = argparse.ArgumentParser(
        description='Front to the imdoing commands.')
    parser.add_argument('command',
                        type=str,
                        help='the imdoing command to run',
                        choices=["mine", "list", "current", "create", "update",
                                 "assign", "status", "start", "stop", "time",
                                 "export", "timesheet"])
    parser.add_argument('arguments',
                        nargs=argparse.REMAINDER,
                        help='the command arguments')
    args = parser.parse_args()
    return args.command, args.arguments


def get_dir():
    directory = os.environ.get('TEAM_PATH')

    if not directory:
        print "The environment variable TEAM_PATH is not set. Aborting."
        sys.exit()

    return os.path.join(directory, "imdoing")


def get_api_key():
    api_key = os.environ.get('CHILI_API_KEY')

    if api_key is None:
        print CHILI_ERROR

    return api_key


CHILI_ERROR = """
Sorry, the CHILI_API_KEY environment variable was not set, you cannot \
use the time-tracking features.
To generate the key, please use the link in the left column at
https://support.sysfera.com/my/account
and add the following to your .bashrc (or something):
export CHILI_API_KEY=XXX
"""
TEAM_PATH = get_dir()
configFile = open(os.path.join(TEAM_PATH, os.pardir,
                               'dashboard', 'data',
                               'config.json'))
config = json.load(configFile)
configFile.close()
REGISTER_URL = config['global']['register_url']
URL = config['chili']['url']
COMMON_KEY = config['chili']['api']
PERSONAL_KEY = get_api_key()
USERS = config['chili']['members']
USERNAMES = [str(U['name']) for U in USERS]
CUSTOMER_PROJECTS = config['chili']['customerProjects']
SYSFERA_PROJECTS = config['chili']['sysferaProjects']
TARGET_VERSION = config['chili']['version_id']
TRACKERS = config['chili']['trackers']
STATUSES = config['chili']['statuses']
PRIORITIES = config['chili']['priorities']
SPRINT_START = config['sprint']['start']
SPRINT_END = config['sprint']['end']


def dispatch(command, arguments):
    api_key = PERSONAL_KEY or COMMON_KEY
    rmine = Redmine(URL, key=api_key, requests={'verify': False})

    if command == 'mine':
        mine.run(rmine, arguments, USERNAMES, USERS)

    # current = list
    elif command == 'current':
        current.run(rmine, TARGET_VERSION, USERS)
    elif command == 'list':
        current.run(rmine, TARGET_VERSION, USERS)

    elif command == 'create':
        create.run(rmine, arguments, TARGET_VERSION, USERS, TRACKERS,
                   PRIORITIES, CUSTOMER_PROJECTS+SYSFERA_PROJECTS, STATUSES)

    elif command == 'update':
        update.run(rmine, arguments, USERS, STATUSES, PRIORITIES, TRACKERS)

    elif command == 'time':
        if PERSONAL_KEY:
            timelog.run(rmine, arguments)

    elif command == 'export':
        if PERSONAL_KEY:
            export.run(rmine, SPRINT_START, SPRINT_END, USERS, TEAM_PATH)

    elif command == 'timesheet':
        if PERSONAL_KEY:
            timesheet.run(rmine, arguments, USERS)

    elif command == 'start':
        mytime.run(rmine, arguments, TEAM_PATH, "start", USERS, STATUSES)
    elif command == 'stop':
        mytime.run(rmine, arguments, TEAM_PATH, "stop", USERS, STATUSES)

    # deprecated commands
    elif command == 'assign':
        assign.run(arguments, USERNAMES)
    elif command == 'status':
        status.run(arguments, STATUSES)

    sys.exit()


def main():
    c, a = parse_command_line()
    dispatch(c, a)


if __name__ == '__main__':
    main()
