#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

from datetime import datetime
import os
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
# pip install python-dateutil

USERS = config['chili']['members']
USERNAMES = [str(U['name']) for U in USERS]

parser = argparse.ArgumentParser(description='Start or stop work on a ticket.')
parser.add_argument('action', type=str,
                    help='the action to record',
                    choices=["start", "stop"])
parser.add_argument('ticket', type=int,
                    help='the ticket # being worked on')
parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                    help='who starts/stops working',
                    choices=USERNAMES)
args = parser.parse_args()

USER = args.user
ACTION = args.action
TICKET = args.ticket
NOW = datetime.now()
DATE = "%(Y)d.%(m)02d.%(d)02d-%(H)02d:%(M)02d:%(S)02d" % {"Y": NOW.year, "m": NOW.month, "d": NOW.day,
                                                          "H": NOW.hour, "M": NOW.minute, "S": NOW.second}


def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_log(directory, date, user, ticket, action):
    basename = '%(date)s-%(user)s-%(ticket)d-%(action)s' % {"directory": directory, "date": date, "user": user,
                                                            "ticket": ticket, "action": action}
    filename = os.path.join(directory, basename)

    if not os.path.isfile(filename):
        try:
            open(filename, 'w').close()
            print '%(user)s %(action)ss working on ticket #%(ticket)d' % {"user": user, "action": action, "ticket": ticket}
        except IOError, e:
            print 'There was an error starting the log.'
            print e
    else:
        print "The file already exists. As this is highly unlikely, something bad is probably going on ;)"


def main():
    directory = os.path.join(get_dir(), "timelog", USER)
    check_dir(directory)
    write_log(directory, DATE, USER, TICKET, ACTION)


if __name__ == '__main__':
    main()