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

TRACKERS = {
    "bug": 1,
    "enhancement": 2,
    "support": 3,
    "team": 4
}



def create(redmine, parent, subject, desc, tracker, target):
    status_id = 1  # New
    start_date = datetime.now(dateutil.tz.tzutc())

    description = desc
    tracker_id = TRACKERS[tracker]

    parent_issue_id = parent
    parent_issue = redmine.issue.get(parent)
    project_id = parent_issue['project']['id']
    of = [cf['value'] for cf in parent_issue['custom_fields'] if cf['name'] == "OF"][0]
    fixed_version_id = target
    custom_fields = [
        {
            'id': 5,
            'value': str(of)
        }
    ]

    ticket = redmine.issue.create(project_id=project_id,
                                  subject=subject,
                                  tracker_id=tracker_id,
                                  description=description,
                                  status_id=status_id,
                                  start_date=start_date,
                                  parent_issue_id=parent_issue_id,
                                  custom_fields=custom_fields,
                                  fixed_version_id=fixed_version_id)

    return ticket


def run(rmine, arguments, users, target):
#    rmine = Redmine(URL, key=API, requests={'verify': False})
    parent = ''
    subject = ''
    desc = ''
    tracker = ''
    user = getpass.getuser()
    userid = [U['id'] for U in users if U['name'] == user][0]
    try:
        opts, args = getopt.getopt(arguments, "p:s:d:t:", "parent,subject,description,tracker")
    except getopt.GetoptError:
        print 'Error checking options for mine'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--parent"):
            parent = arg
        if opt in ("-s", "--subject"):
            subject = arg
        if opt in ("-d", "--description"):
            desc = arg
        if opt in ("-t", "--tracker"):
            tracker = arg

    if parent == '' or subject == '' or desc == '' or tracker == '':
        print 'Error missing IN parameter'
        print 'Usage: imdoing create -p parent -s subject -d desc -t tracker'
        sys.exit(2)


    issue = create(rmine, parent, subject, desc, tracker, target)
    print "Issue #" + str(issue['id']) + " was created by " + user
    print "https://support.sysfera.com/issues/" + str(issue['id'])

