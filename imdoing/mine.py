# ~*~ coding: utf-8 ~*~
from variables import *


def data(userid):
    results = []

    for issue in REDMINE.issue.filter(assigned_to_id=userid):
        cf_of = [cf['value'] for cf in issue['custom_fields']
                 if cf['name'] == "OF"][0]
        of = "None" if cf_of == "" else str(cf_of)

        result = {
            'id': issue['id'],
            'subject': issue['subject'],
            'of': of
        }

        results.append(result)

    return results


def add_parser(subparsers):
    fdt_parser = subparsers.add_parser('mine',
                                       help='List the tickets assigned to '
                                            'a user')

    fdt_parser.add_argument('user',
                            nargs='?',
                            default=CURRENT_USER,
                            type=str,
                            help='the user to whom tickets are assigned '
                                 '(default: you)')


def display(user, tickets):
    print u"Tickets assigned to user {}:".format(user)
    if len(tickets) > 0:
        for ticket in tickets:
            print u"#{id} === OF: {of} === {subject}".format(**ticket)
    else:
        print u"No ticket found. Maybe you meant another user?"


def run(args):
    user = args.user
    user_id = USERNAMES[user]

    tickets = data(user_id)

    display(user, tickets)