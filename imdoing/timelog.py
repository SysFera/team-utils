# ~*~ coding: utf-8 ~*~
from variables import *


def register(options):
    if REDMINE.time_entry.create(**options):
        print u'You worked {hours} hours on {spent_on} for ticket:' \
              u'\nhttps://support.sysfera.com/issues/{issue_id}\n' \
            .format(**options)
    else:
        print u"There was an error saving your entry, please try again."


def add_parser(subparsers):
    subparser = subparsers.add_parser('time',
                                      help='Log time on a ticket.')

    subparser.add_argument('issue_id',
                           type=int,
                           help='the ticket you worked on')

    subparser.add_argument('hours',
                           type=float,
                           help='the number of hours worked')

    subparser.add_argument('--comments', '-c',
                           type=str,
                           help='comments to add to the time entry')

    subparser.add_argument('--date', '-d',
                           type=str,
                           default=DATE,
                           help='the date (format: "YYYY-MM-DD"), '
                                'defaults to today')


def run(args):
    if PERSONAL_KEY:
        options = {
            'issue_id': args.issue_id,
            'hours': args.hours,
            'spent_on': args.date,
            'activity_id': 9,
            'comments': args.comments
        }

        register(options)