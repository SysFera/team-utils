#!/usr/bin/python
# ~*~ coding: utf-8 ~*~
import os

from redmine import Redmine
import json
import getpass
import argparse
import imdoing
import sys
import getopt

def data(redmine, userid):
    results = []

    for issue in redmine.issue.filter(assigned_to_id=userid):
        of = [cf['value'] for cf in issue['custom_fields'] if cf['name'] == "OF"][0]
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
    try:
        opts, args = getopt.getopt(arguments, "u:", "user")
    except getopt.GetoptError:
        print 'Error checking options for mine'
        sys.exit(2)
    userid = ""
    user = getpass.getuser()
    for opt, arg in opts:
        if opt in ("-u", "--user"):
            user = arg
    userid = [U['id'] for U in users if U['name'] == user]
    tickets = data(redmine, userid)
    print "Tickets assigned to user " + user + ":"
    if len(tickets) > 0:
        for ticket in tickets:
            print "#" + str(ticket['number']) + " === OF: " + ticket['of'] + " === " + ticket['subject']
    else:
        print "No ticket found. Maybe you meant another user?"


