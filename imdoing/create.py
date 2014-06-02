#!/usr/bin/python
# ~*~ coding: utf-8 ~*~
from datetime import datetime
import dateutil.parser
import argparse


def create(redmine, parent, project, subject, desc, tracker, target, priority, of):
    status_id = 1  # New
    start_date = datetime.now(dateutil.tz.tzutc())
    description = desc
    tracker_id = tracker
    fixed_version_id = target

    if project == '':  # project was not set, let's use the provided parent ticket
        parent_issue_id = parent
        parent_issue = redmine.issue.get(parent)
        project_id = parent_issue['project']['id']
        if of == 0:
            of = [cf['value'] for cf in parent_issue['custom_fields'] if cf['name'] == "OF"][0]

    if parent == 0:  # parent was not set, let's use the provided project
        parent_issue_id = None
        project_id = project

    custom_fields = [
        {
            'id': 5,
            'value': str(of) if not of == 0 else ''
        }
    ]

    ticket = redmine.issue.create(project_id=project_id,
                                  subject=subject,
                                  priority_id=priority,
                                  tracker_id=tracker_id,
                                  description=description,
                                  status_id=status_id,
                                  start_date=start_date,
                                  parent_issue_id=parent_issue_id,
                                  custom_fields=custom_fields,
                                  fixed_version_id=fixed_version_id)

    return ticket


def run(rmine, arguments, target, user, trackers, priorities, projects):
    parser = argparse.ArgumentParser(description='Create a new ticket.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--parent', type=int)
    group.add_argument('-P', '--project', type=str, choices=[project['name'] for project in projects])
    parser.add_argument('-s', '--subject', type=str, required=True)
    parser.add_argument('-d', '--description', type=str, required=True)
    parser.add_argument('-t', '--tracker', type=str, choices=trackers.keys(), required=True)
    parser.add_argument('--priority', type=str, default="normal", choices=priorities.keys())
    parser.add_argument('--of', type=int, default=0)
    args = parser.parse_args(arguments)

    of = args.of
    desc = args.description
    subject = args.subject
    tracker = trackers[args.tracker]
    priority = priorities[args.priority]
    project = args.project or ''
    parent = args.parent or 0

    issue = create(rmine, parent, project, subject, desc, tracker, target, priority, of)
    print "Issue #" + str(issue['id']) + " was created by " + user
    print "https://support.sysfera.com/issues/" + str(issue['id'])