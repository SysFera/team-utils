# ~*~ coding: utf-8 ~*~
from datetime import datetime
import os
import getpass
import argparse


format_string = u"{0.year}-{0.month:02}-{0.day:02}"
NOW = datetime.now()
DATE = format_string.format(NOW)


def parse_filename(f):
    comments = open(f, 'r').read()
    filename = os.path.basename(f)
    data = filename.split(".")
    issue_id = data[0]
    hours = data[1]
    user = data[2]
    date = data[3]

    return {
        'issue_id': issue_id,
        'hours': hours,
        'user_id': usernames[user],
        'spent_on': date,
        'activity_id': 9,
        'comments': comments
    }


def check_dir():
    if not os.path.exists(timelog_dir):
        os.makedirs(timelog_dir)


def check_backlog():
    try:
        ls = os.listdir(timelog_dir)
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
                options = parse_filename(f)
                register(options, False)


def register_local(options):
    check_dir()
    basename = u'{issue_id}.{hours}.{user_id}.{spent_on}'.format(**options)
    filename = os.path.join(timelog_dir, basename)

    if not os.path.isfile(filename):
        try:
            f = open(filename, 'w')
            with f:
                f.write(options['comments'])
                os.utime(filename, None)
            print u'{user_id} worked {hours} hours on {spent_on} for ' \
                  u'ticket #{issue_id} (registered locally)'.format(**options)
        except IOError as e:
            print 'There was an error writing the log to the filesystem.'
            print e
    else:
        print "The file already exists. As this is highly unlikely, " \
              "something bad is probably going on ;)"


def log_time(options):
    return redmine.time_entry.create(**options)


def register(options, backlog=True):
    # try to save remotely, do it locally if it fails
    print "\nTrying to register on the server...",
    user = options.pop("user")

    if log_time(options):
        print "Success =)"
        print u'{0} worked {hours} hours on {spent_on} for ticket:' \
              u'\nhttps://support.sysfera.com/issues/{issue_id}\n'\
            .format(user, **options)
        if backlog:
            check_backlog()
    else:
        print 'Failed. Saving locally.'
        register_local(options)


def parse_args(arguments):
    # we create sorted lists for options
    usernames_s = sorted([username for username in usernames.iterkeys()])

    # we create the parser
    parser = argparse.ArgumentParser(description='Log time on a ticket.')
    parser.add_argument('issue_id', type=int,
                        help='the ticket # being worked on')
    parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                        help='who starts/stops working', choices=usernames_s)
    parser.add_argument('--hours', type=float, required=True,
                        help='the number of hours worked')
    parser.add_argument('--date', type=str, default=NOW,
                        help='the date (format: YYYY-MM-DD)')
    parser.add_argument('--comments', type=str,
                        help='comments to add to the time entry')

    return parser.parse_args(arguments)


def run(rmine, arguments, team_path, users):
    global redmine, usernames, timelog_dir
    redmine = rmine

    # we create a mapping [username: id]
    usernames = {user['name']: user['id'] for user in users}
    usernames['nobody'] = 0

    args = parse_args(arguments)

    timelog_dir = os.path.join(team_path, "timelog")

    user = args.user
    options = {
        'issue_id': args.issue_id,
        'hours': args.hours,
        'user': user,
        'user_id': usernames[user],
        'spent_on': format_string.format(args.date),
        'activity_id': 9,
        'comments': args.comments
    }

    register(options)