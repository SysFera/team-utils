#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

from datetime import datetime
import os
import dateutil.parser
import json
import getpass
import argparse


NOW = datetime.now()
DATE = "{0.year}.{0.month:02}.{0.day:02}-{0.hour:02}:{0.minute:02}:{0.second:02}".format(NOW)


def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_log(directory, date, user, ticket, action):
    basename = '{}-{}-{}-{}'.format(date, user, ticket, action)
    filename = os.path.join(directory, basename)

    if not os.path.isfile(filename):
        try:
            open(filename, 'w').close()
            print '{} {} working on ticket #{}'.format(user, action, ticket)
        except IOError, e:
            print 'There was an error starting the log.'
            print e
    else:
        print "The file already exists. As this is highly unlikely, something bad is probably going on ;)"


def run(arguments, users, direc, action, usernames):
    parser = argparse.ArgumentParser(description='Start or stop work on a ticket.')
    parser.add_argument('action', type=str,
                        help='the action to record',
                        choices=["start", "stop"])
    parser.add_argument('ticket', type=int,
                        help='the ticket # being worked on')
    parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                        help='who starts/stops working',
                        choices=usernames)
    args = parser.parse_args()
    
    user = args.user
    action = args.action
    ticket = args.ticket
    userid = [U['id'] for U in users if U['name'] == user]

    directory = os.path.join(direc, "timelog", user)
    check_dir(directory)
    write_log(directory, DATE, user, ticket, action)

