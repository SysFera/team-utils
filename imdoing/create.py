#!/usr/bin/python
# ~*~ coding: utf-8 ~*~
from datetime import datetime
import dateutil.parser
import argparse


def create(redmine, parent, subject, desc, tracker, target):
    status_id = 1  # New
    start_date = datetime.now(dateutil.tz.tzutc())
    description = desc
    tracker_id = tracker
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


def run(rmine, arguments, target, user, trackers):
    parser = argparse.ArgumentParser(description='Create a new ticket.')
    parser.add_argument('-p', '--parent', type=int, required=True)
    parser.add_argument('-s', '--subject', type=str, required=True)
    parser.add_argument('-d', '--description', type=str, required=True)
    parser.add_argument('-t', '--tracker', type=str, choices=["bug", "enhancement", "support", "team"],
                        required=True)
    args = parser.parse_args(arguments)
    parent = args.parent
    desc = args.description
    subject = args.subject
    tracker = trackers[args.tracker]

    issue = create(rmine, parent, subject, desc, tracker, target)
    print "Issue #" + str(issue['id']) + " was created by " + user
    print "https://support.sysfera.com/issues/" + str(issue['id'])

