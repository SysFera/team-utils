# ! /usr/bin/python
# ~*~ coding: utf-8 ~*~

from redmine import Redmine
from collections import Counter
from datetime import datetime
import dateutil.parser
import json

configFile = open('config.json')
config = json.load(configFile)
configFile.close()

# non-standard modules required
# pip install python-redmine
# pip install python-dateutil

URL = config['chili']['url']
API = config['chili']['api']

FILE_PROJECTS = config['chili']['fileProjects']
FILE_TEAM = config['chili']['fileTeam']

CUSTOMER_PROJECTS = config['chili']['customerProjects']
SYSFERA_PROJECTS = config['chili']['sysferaProjects']
MEMBERS = [M['id'] for M in config['chili']['members']]

SPRINT_TARGET = "%02d" % config['sprint']['end']['day'] + "-" + "%02d" % config['sprint']['end']['month'] + "-" + "%04d" % config['sprint']['end']['year']
# SPRINT_TARGET = config['sprint']['version_id']
TRACKER = config['sprint']['trackers']['bug']


def sort_collection_by_name(collection):
    return sorted(collection, key=lambda collection: collection['name'].lower)


def create_user_list():
    users = []

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
        users.append(user)

    return users


def add_issues_to_users(users, issues):
    for issue in issues:
        if hasattr(issue, 'assigned_to'):
            status = issue.status['id']
            assignee = issue['assigned_to']['id']

            if assignee in MEMBERS:
                user = [user for user in users if (user['id'] == assignee)][0]
                if status == 1:
                    user['issues']['new'] += 1
                if status == 2:
                    user['issues']['open'] += 1
                if status == 5:
                    user['issues']['closed'] += 1
    return


def get_issues(p, attr, field, value):
    issues_id = []
    for i in p.issues:
        if hasattr(i, attr):
            a = getattr(i, attr)
            if getattr(a, field) == value:
                issues_id.append(i.id)
    return p.issues.filter(issues_id)


def create_project_json(p, issues, deadline):
    total = len(issues)
    counter = Counter([i.status.name for i in issues])

    return {
        'name': p.name,
        'total': total,
        'open': counter[u'En cours'] + counter[u'Nouveau'],
        'new': counter[u'Nouveau'],
        'closed': counter[u'Résolu'] + counter[u'Fermé'] + counter[u'Rejeté'],
        'deadline': deadline
    }


def data(redmine):
    customer_projects = []
    sysfera_projects = []
    users = create_user_list()

    for p in redmine.project.all():
        if p.name in [x['name'] for x in SYSFERA_PROJECTS]:
            issues = get_issues(p, "fixed_version", "name", SPRINT_TARGET)
            project = create_project_json(p, issues, 0)
            add_issues_to_users(users, p.issues)
            sysfera_projects.append(project)
        elif p.name in [x['name'] for x in CUSTOMER_PROJECTS]:
            issues = get_issues(p, "tracker", "id", TRACKER)
            now = datetime.now(dateutil.tz.tzutc())
            elapsed = [int(round((now - dateutil.parser.parse(issue.created_on)).total_seconds() // 3600))
                       for issue in issues if issue.status.name == u'Nouveau']
            deadline = max(elapsed) if elapsed else 0
            project = create_project_json(p, issues, deadline)
            add_issues_to_users(users, p.issues)
            customer_projects.append(project)

    team = {
        "users": sorted(users, key=lambda user: user["name"])
    }

    projects = {
        "sysfera": sort_collection_by_name(sysfera_projects),
        "customers": sort_collection_by_name(customer_projects)
    }

    return {
        "team": team,
        "projects": projects
    }

if __name__ == '__main__':
    rmine = Redmine(URL, key=API, requests={'verify': False})
    result = data(rmine)
    data_file = open(FILE_TEAM, 'w')
    jsonified = json.dump(result['team'], data_file, indent=4)
    data_file = open(FILE_PROJECTS, 'w')
    jsonified = json.dump(result['projects'], data_file, indent=4)
