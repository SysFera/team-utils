# ~*~ coding: utf-8 ~*~
from datetime import datetime
import argparse


format_string = u"{0.year}-{0.month:02}-{0.day:02}"
NOW = datetime.now()
DATE = format_string.format(NOW)


def register(options):
    if redmine.time_entry.create(**options):
        print u'You worked {hours} hours on {spent_on} for ticket:' \
              u'\nhttps://support.sysfera.com/issues/{issue_id}\n' \
            .format(**options)
    else:
        print "There was an error saving your time entry, please try again."


def parse_args(arguments):
    parser = argparse.ArgumentParser(description='Log time on a ticket.')
    parser.add_argument('issue_id', type=int,
                        help='the ticket # being worked on')
    parser.add_argument('hours', type=float,
                        help='the number of hours worked')
    parser.add_argument('--date', '-d', type=str, default=NOW,
                        help='the date (format: "YYYY-MM-DD"), defaults to'
                             'today')
    parser.add_argument('--comments', '-c', type=str,
                        help='comments to add to the time entry')

    return parser.parse_args(arguments)


def run(rmine, arguments):
    global redmine
    redmine = rmine

    args = parse_args(arguments)

    options = {
        'issue_id': args.issue_id,
        'hours': args.hours,
        'spent_on': args.date,
        'activity_id': 9,
        'comments': args.comments
    }

    register(options)