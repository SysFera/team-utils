# ~*~ coding: utf-8 ~*~
from datetime import datetime
import os
import getpass
import argparse
import json, requests


SERVER = 'http://localhost:8080/'
NOW = datetime.now()
DATE = u"{0.year}.{0.month:02}.{0.day:02}-{0.hour:02}:{0.minute:02}:{0.second:02}".format(NOW)


def register_file(f):
    return f


def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def check_backlog(directory):
    try:
        ls = os.listdir(directory)
    except IOError as e:
        print "Error listing files:", e
        print "Aborting backlog."
    else:
        if len(ls) == 0:
            print "Backlog is empty, nothing to do!"
        else:
            print "Backlog needs emptying, let's do it!"
            for f in ls:
                print "Trying to register file", f
                register_file(f)


def register_local(directory, timestamp):
    check_dir(directory)
    basename = u'{date}-{user}-{ticket}-{action}'.format(**timestamp)
    filename = os.path.join(directory, basename)

    if not os.path.isfile(filename):
        try:
            with open(filename, 'w'):
                os.utime(filename, None)
            print u'{user} {action}s working on ticket #{ticket} at {date} (registered locally)'.format(**timestamp)
        except IOError as e:
            print 'There was an error writing the log to the filesystem.'
            print e
    else:
        print "The file already exists. As this is highly unlikely, something bad is probably going on ;)"


def register(directory, timestamp):  # try to save remotely, do it locally if it fails
    url = SERVER + 'register'
    data = json.dumps(timestamp)

    print "Trying to register on the server...",

    try:
        req = requests.post(url, data)
    except IOError:
        print 'Failed (could not reach the server). Saving locally.'
        register_local(directory, timestamp)
    else:
        if req.status_code == 200:
            print "Success =)"
            print req.text
            check_backlog(directory)
        else:
            print "Failed (the server returned an error). Saving locally."
            register_local(directory, timestamp)


def run(arguments, direc, action, usernames):
    parser = argparse.ArgumentParser(description='Start or stop work on a ticket.')
    parser.add_argument('ticket', type=int,
                        help='the ticket # being worked on')
    parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                        help='who starts/stops working',
                        choices=usernames)
    args = parser.parse_args(arguments)
    user = args.user
    ticket = args.ticket

    directory = os.path.join(direc, "timelog")
    timestamp = {
        'user': user,
        'ticket': ticket,
        'action': action,
        'date': DATE
    }

    register(directory, timestamp)

