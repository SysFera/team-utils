#!/usr/bin/python
# ~*~ coding: utf-8 ~*~
import os

from redmine import Redmine
from datetime import datetime
import dateutil.parser
import json
import getpass
import argparse


def get_dir():
    directory = os.environ.get('TEAM_PATH')

    if directory is not None:
        return os.path.join(directory, "imdoing")
    else:
        print "The environment variable TEAM_PATH is not set. Aborting."
        quit()


configFile = open(os.path.join(get_dir(), 'config.json'))
config = json.load(configFile)
configFile.close()

# non-standard modules required
# pip install python-redmine
# pip install python-dateutil

URL = config['chili']['url']
API = config['chili']['api']
USERS = config['chili']['members']
USERNAMES = [str(U['name']) for U in USERS]

parser = argparse.ArgumentParser(description='Assign a ticket to self or to $user.')
parser.add_argument('ticket', type=int,
                    help='the ticket number')
parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                    help='the user to whom tickets are assigned',
                    choices=USERNAMES)
args = parser.parse_args()
TICKET = args.ticket
USER = args.user
USER_ID = [U['id'] for U in USERS if U['name'] == USER][0]


def assign(redmine):
    status_id = 2  # Open

    ticket = redmine.issue.update(TICKET, assigned_to_id=USER_ID, status_id=status_id)

    return ticket


def main():
    rmine = Redmine(URL, key=API, requests={'verify': False})
    if assign(rmine):
        print "Issue #" + str(TICKET) + " was successfully assigned to " + USER
        print "https://support.sysfera.com/issues/" + str(TICKET)
    else:
        print "There was an error assigning issue #" + str(TICKET) + " to " + USER


if __name__ == '__main__':
    main()