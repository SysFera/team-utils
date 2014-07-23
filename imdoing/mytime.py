# ~*~ coding: utf-8 ~*~
from datetime import datetime
import os
import getpass
import argparse
import json
import requests

NOW = datetime.now()
DATE = u"{0.year}.{0.month:02}.{0.day:02}-{0.hour:02}:{0.minute:02}:{0.second:02}".format(NOW)


def parse_filename(f):
    filename = os.path.basename(f)
    data = filename.split("-")
    date = data[0] + "-" + data[1]
    user = data[2]
    ticket = data[3]
    action = data[4]

    return {
        'date': date,
        'user': user,
        'action': action,
        'ticket': ticket
    }


def register_file(f):  # returns 0 if server unreachable, 1 if operation failed, 2 if operation OK
    timestamp = parse_filename(f)
    data = json.dumps(timestamp)

    try:
        req = requests.post(REGISTER_URL, data)
    except IOError:
        print "Failed (server unreachable). File was kept."
        return 0
    else:
        if req.status_code == 200:
            print "Success =)"
            print req.text
            return 2
        else:
            print "Failed (server returned an error). File was kept."
            return 1


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
            return False
        else:
            print "Backlog needs emptying, let's do it!"
            for f in ls:
                print "Trying to register file", f, "...",
                server_reachable = register_file(f)
                if server_reachable == 0:
                    break
                elif server_reachable == 2:
                    try:
                        os.remove(os.path.join(directory, f))
                    except IOError:
                        print "Could not remove the file, it was kept."


def register_local(directory, timestamp):
    check_dir(directory)
    basename = u'{date}-{user}-{ticket}-{action}'.format(**timestamp)
    filename = os.path.join(directory, basename)

    if not os.path.isfile(filename):
        try:
            with open(filename, 'w'):
                os.utime(filename, None)
            print u'{user} {action}s working on ticket #{ticket} at ' \
                  u'{date} (registered locally)'.format(**timestamp)
        except IOError as e:
            print 'There was an error writing the log to the filesystem.'
            print e
    else:
        print "The file already exists. As this is highly unlikely, " \
              "something bad is probably going on ;)"


def register(directory, timestamp):
    # try to save remotely, do it locally if it fails
    server_reachable = True
    data = json.dumps(timestamp)

    print "Trying to register on the server...",

    try:
        req = requests.post(REGISTER_URL, data)
    except IOError:
        print 'Failed (server unreachable). Saving locally.'
        server_reachable = False
        register_local(directory, timestamp)
    else:
        if req.status_code == 200:
            print "Success =)"
            print req.text
        else:
            print "Failed (server returned an error). Saving locally."
            register_local(directory, timestamp)

    if server_reachable:
        check_backlog(directory)


def run(arguments, direc, action, usernames, register_url):
    global REGISTER_URL
    REGISTER_URL = register_url
    parser = argparse.ArgumentParser(description='Start or stop work '
                                                 'on a ticket.')
    parser.add_argument('ticket', type=int,
                        help='the ticket # being worked on')
    parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                        help='who starts/stops working', choices=usernames)
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