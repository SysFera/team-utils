# ! /usr/bin/python
# ~*~ coding: utf-8 ~*~

from redmine import Redmine
from datetime import datetime
import dateutil.parser
import json
import getpass
import argparse

configFile = open('config.json')
config = json.load(configFile)
configFile.close()

# non-standard modules required
# pip install python-redmine
# pip install python-dateutil

URL = config['chili']['url']
API = config['chili']['api']
USERS = config['chili']['members']
TARGET_VERSION = config['sprint']['version_id']

TRACKERS = {
    "bug": 1,
    "enhancement": 2,
    "support": 3,
    "team": 4
}

parser = argparse.ArgumentParser(description='Create a new ticket.')
parser.add_argument('-p', '--parent', nargs='?', type=int, required=True)
parser.add_argument('-s', '--subject', nargs='?', type=str, required=True)
parser.add_argument('-d', '--description', nargs='?', type=str, required=True)
parser.add_argument('-t', '--tracker', nargs='?', type=str, choices=["bug", "enhancement", "support", "team"],
                    required=True)
args = parser.parse_args()

PARENT = args.parent
SUBJECT = args.subject
DESC = args.description
TRACKER = args.tracker

USER = getpass.getuser()
USER_ID = [U['id'] for U in USERS if U['name'] == USER][0]


def create(redmine):
    status_id = 1  # New
    start_date = datetime.now(dateutil.tz.tzutc())

    subject = SUBJECT
    description = DESC
    tracker_id = TRACKERS[TRACKER]
    assigned_to_id = USER_ID

    parent_issue_id = PARENT
    parent_issue = redmine.issue.get(PARENT)
    project_id = parent_issue['project']['id']
    of = [cf['value'] for cf in parent_issue['custom_fields'] if cf['name'] == "OF"][0]
    fixed_version_id = TARGET_VERSION
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
                                  assigned_to_id=assigned_to_id,
                                  parent_issue_id=parent_issue_id,
                                  custom_fields=custom_fields,
                                  fixed_version_id=fixed_version_id)

    return ticket


if __name__ == '__main__':
    rmine = Redmine(URL, key=API, requests={'verify': False}, impersonate="aragon")
    # create(rmine)
    issue = create(rmine)
    print "Issue #" + str(issue['id']) + " was created by " + USER