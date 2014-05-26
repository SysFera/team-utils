#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

import getpass
import argparse


def assign(redmine, userid, ticket):
    status_id = 2  # Open
    ticket = redmine.issue.update(ticket, assigned_to_id=userid[0],
                                  status_id=status_id)
    return ticket


def run(rmine, arguments, users, usernames):
    parser = argparse.ArgumentParser(
        description='Assign a ticket to self or to $user.')
    parser.add_argument('ticket', type=int,
                        help='the ticket number')
    parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                        help='the user to whom tickets are assigned',
                        choices=usernames)
    args = parser.parse_args(arguments)
    ticket = args.ticket
    user = args.user

    userid = [U['id'] for U in users if U['name'] == user]

    if assign(rmine, userid, ticket):
        print u"Issue #{} was successfully assigned to {}".format(ticket, user)
        print u"https://support.sysfera.com/issues/{}".format(ticket)
    else:
        print u"There was an error assigning issue #{} to {}".format(ticket, user)

