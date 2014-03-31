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
DATA_FILE = "dataProjects.json"
INTERNAL_PROJECTS = ["SysFera", "SysFera-marketing"]

def sortCollectionByName(collection):
    return sorted(collection, key=lambda collection: collection['name'].lower)

def data(rmine):
    """List projects"""
    projetsClient = []
    projetsSysFera = []

    for x in rmine.project.all():
        # bugfix: project API does not retrieve all associated tickets
        # even if limit is raised
        issues = rmine.issue.all(project_id=x.id,
                                 status_id="*")
        total = len(issues)
        counter = Counter([i.status.name for i in issues])
        now = datetime.now(dateutil.tz.tzutc())
        # compute elapsed time between ticket creation
        elapsed = [int(round((now - dateutil.parser.parse(issue.created_on)).total_seconds() // 3600))
               for issue in issues if issue.status.name == 'Nouveau']

        deadline = max(elapsed) if elapsed else 0
        project = { 
            'name': x.name,
            'total': total,
            'open': counter['En cours'] + counter['Nouveau'], 
            'new': counter['Nouveau'],
            'closed': counter[u'Résolu'] + counter[u'Fermé'] + counter[u'Rejeté'],
            'deadline': deadline
        }
        if x.name in INTERNAL_PROJECTS:
            projetsSysFera.append( project )
        else:
            projetsClient.append( project )

    res = { "projetsClient": sortCollectionByName(projetsClient), "projetsSysFera": sortCollectionByName(projetsSysFera)}
    return res

if __name__ == '__main__':
    rmine = Redmine(SITE_URL, key=API_KEY, requests={ 'verify': False })
    result = data(rmine)
    data_file = open(DATA_FILE, 'w')
    jsonified = json.dump(result, data_file, indent=4)
