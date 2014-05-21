# ! /usr/bin/python
# ~*~ coding: utf-8 ~*~

from datetime import datetime
import os
import dateutil.parser
import json
import getpass
import argparse

configFile = open('config.json')
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

DIR = "timelog"
USER = args.user
ACTION = args.action
TICKET = args.ticket
NOW = datetime.now(dateutil.tz.tzutc())
DATE = "%(Y)d.%(m)02d.%(d)02d-%(H)02d:%(M)02d:%(S)02d" % {"Y": NOW.year, "m": NOW.month, "d": NOW.day,
                                                          "H": NOW.hour, "M": NOW.minute, "S": NOW.second}


def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def check_ticket_exists():
    return True


def check_ticket_started():
    return True


if __name__ == '__main__':
    check_dir(DIR)
    filename = '%(DIR)s/%(DATE)s-%(USER)s-%(TICKET)d-%(ACTION)s' % {"DIR": DIR, "DATE": DATE, "USER": USER, "TICKET": TICKET,
                                                            "ACTION": ACTION}
    print 'User %(USER)s wants to %(ACTION)s working on ticket #%(TICKET)d' % {"USER": USER, "ACTION": ACTION,
                                                                               "TICKET": TICKET}

    data_file = open(filename, 'w')