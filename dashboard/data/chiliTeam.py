#! /usr/bin/python
# ~*~ coding: utf-8 ~*~

from redmine import Redmine
from collections import Counter
from datetime import datetime
import dateutil.parser
import json
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

# non-standard modules required
# pip install python-redmine
# pip install python-dateutil

URL = config.get('Chili', 'URL')
API = config.get('Chili', 'API')
FILE = config.get('Chili', 'FILE')
MEMBERS = eval(config.get('Chili', 'MEMBERS'))

def data(rmine):
    members = []
    for memberId in MEMBERS:
        member = rmine.user.get(memberId)
        user = {
            'id': memberId,
            'name': member.firstname,
            'issues': {
                'new': 0,
                'open': 0,
                'closed': 0
            }
        }

        issues = rmine.issue.filter(assigned_to_id=memberId)
        for issue in issues:
            status = issue.status['id']
            if status == 1:
                user['issues']['new'] += 1
            if status == 2:
                user['issues']['open'] += 1
            if status == 3:
                user['issues']['closed'] += 1
            if status == 5:
                user['issues']['closed'] += 1
            if status == 6:
                user['issues']['closed'] += 1

        members.append( user )

    res = { 'members': sorted(members, key=lambda member: member['name']) }
    return res

if __name__ == '__main__':
    rmine = Redmine(URL, key=API, requests={ 'verify': False })
    result = data(rmine)
    data_file = open(FILE, 'w')
    jsonified = json.dump(result, data_file, indent=4)
