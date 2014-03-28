#! /usr/bin/python
# ~*~ coding: utf-8 ~*~

from redmine import Redmine
from collections import Counter
from datetime import datetime
import dateutil.parser
import json

# non-standard modules required
# pip install redmine
# pip install python-dateutil

SITE_URL = "https://support.sysfera.com"
API_KEY = "28ae1810e982c8a2a1f4f4b726e1feced351e229"
DATA_FILE = "dataTeam.json"
MEMBERS = [10,13,17,19,20,22,23,25,29,32]

def data(rmine):
    members = []
    for memberId in MEMBERS:
        member = rmine.user.get(memberId)
        print member
        user = {
            'id': memberId,
            'name': member.firstname + " " + member.lastname,
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
    res = { 'members': members }
    return res

if __name__ == '__main__':
    rmine = Redmine(SITE_URL, key=API_KEY, requests={ 'verify': False })
    result = data(rmine)
    data_file = open(DATA_FILE, 'w')
    jsonified = json.dump(result, data_file, indent=4)
