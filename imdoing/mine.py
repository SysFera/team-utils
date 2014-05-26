#!/usr/bin/python
# ~*~ coding: utf-8 ~*~
import os

from redmine import Redmine
import json
import getpass
import argparse
import imdoing


def data(redmine, userid):
    results = []

    for issue in redmine.issue.filter(assigned_to_id=userid):
        of = [cf['value'] for cf in issue['custom_fields']
              if cf['name'] == "OF"][0]
        if of == '':
            of = "None"
        else:
            of = str(of)

        result = {
            'number': issue['id'],
            'subject': issue['subject'],
            'of': of
        }
        results.append(result)

    return results


def run(redmine, arguments, usernames, users):
    parser = argparse.ArgumentParser(description='List the tickets assigned to self or to $user.')
    parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                        help='the user to whom tickets are assigned',
                        choices=usernames)
    args = parser.parse_args(arguments)
    user = args.user
    userid = [U['id'] for U in users if U['name'] == user]
    tickets = data(redmine, userid)
    print "Tickets assigned to user " + user + ":"
    if len(tickets) > 0:
        for ticket in tickets:
            print "#{} === OF: {} === {}".format(ticket['number'],
                                                 ticket['of'],
                                                 ticket['subject'])
    else:
        print "No ticket found. Maybe you meant another user?"


