#!/usr/bin/python
# ~*~ coding: utf-8 ~*~
import os

from redmine import Redmine
from datetime import datetime
import dateutil.parser
import json
import getpass
import getopt
import sys

def assign(redmine, userid, ticket):
    status_id = 2  # Open
    ticket = redmine.issue.update(ticket, assigned_to_id=userid[0], status_id=status_id)

    return ticket


def run(rmine, arguments, users):
    userid = ""
    user = getpass.getuser()
    ticket = ""
    try:
        opts, args = getopt.getopt(arguments, "u:", "user")
    except getopt.GetoptError:
        print 'Error checking options for mine'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--user"):
            user = arg
    for arg in args:
        try:
            ticket = int(arg)
        except:
            print ""

    userid = [U['id'] for U in users if U['name'] == user]

    if ticket == "" or userid == "":
        print "Missing parameter"
        print "Usage: imdoing assign [-u username]  <ticket_number>"
        sys.exit(2)

    if assign(rmine, userid, ticket):
        print "Issue #" + str(ticket) + " was successfully assigned to " + user
        print "https://support.sysfera.com/issues/" + str(ticket)
    else:
        print "There was an error assigning issue #" + str(ticket) + " to " + user

