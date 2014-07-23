# ~*~ coding: utf-8 ~*~
from datetime import datetime
import os
import getpass
import argparse
import json
import requests
import sys
import imdoing

NOW = datetime.now()
DATE = u"{0.year}.{0.month:02}.{0.day:02}-" \
       u"{0.hour:02}:{0.minute:02}:{0.second:02}".format(NOW)


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


def register_file(f):
    # returns 0 if server unreachable, 1 if operation failed, 2 if operation OK
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


def update_ticket(args, action):
    auto = args.auto
    manual = args.manual
    user = args.user
    ticket_id = args.ticket
    do_update = auto or manual

    if do_update:
        # let's set the default values (used for auto)
        # start is true if action is "start"
        start = action == "start"
        # ticket assigned to the user who starts, or to nobody if stop
        assigned_to = user if start else "nobody"
        # status set to open if start, new if stop
        status = "open" if start else "new"

        # if manual was set, some values may be overridden
        if manual:
            assigned_to = args.assigned_to
            status = args.status
            if not (assigned_to or status):
                print "--manual was set but neither --status nor " \
                      "--assigned_to was set: ticket was not updated.\n" \
                      "Please run 'imdoing update' manually."
                sys.exit()

        c = "update"
        a = [str(ticket_id)]

        if assigned_to is not None:
            a.append("--assigned_to")
            a.append(assigned_to)
        if status is not None:
            a.append("--status")
            a.append(status)

        imdoing.dispatch(c, a)


def run(arguments, direc, action, users, statuses, register_url):
    # REGISTER_URL declared as a global for convenience
    global REGISTER_URL
    REGISTER_URL = register_url

    # we create a mapping [username: id]
    usernames = {user['name']: user['id'] for user in users}
    usernames['nobody'] = 0

    # we create sorted lists for options
    usernames_s = sorted([username for username in usernames.iterkeys()])
    statuses_s = sorted([status for status in statuses.iterkeys()])

    parser = argparse.ArgumentParser(description='Start or stop work '
                                                 'on a ticket.')
    parser.add_argument('ticket', type=int,
                        help='the ticket # being worked on')
    parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                        help='who starts/stops working', choices=usernames_s)

    # options to update the ticket when start/stop
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--auto', '-a', dest='auto', action='store_true',
                       help='automatically update the ticket. '
                            'Start will assign/open the ticket. '
                            'Stop will deassign/new the ticket.')
    group.add_argument('--manual', '-m', dest='manual', action='store_true',
                       help='manually update the ticket')
    parser.add_argument('--status', type=str,
                        help='the status to set. '
                             'Will be ignored if -m is not used.',
                        choices=statuses_s)
    parser.add_argument('--assigned_to', type=str,
                        help='the user to assign the ticket to. '
                             'Will be ignored if -m is not used.',
                        choices=usernames_s)

    args = parser.parse_args(arguments)
    user = args.user
    ticket_id = args.ticket

    timestamp = {
        'user': user,
        'ticket': ticket_id,
        'action': action,
        'date': DATE
    }
    directory = os.path.join(direc, "timelog")
    register(directory, timestamp)

    update_ticket(args, action)