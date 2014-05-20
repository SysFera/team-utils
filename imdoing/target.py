# ! /usr/bin/python
# ~*~ coding: utf-8 ~*~

# non-standard modules required
# pip install python-redmine

from redmine import Redmine
import json

configFile = open('config.json')
config = json.load(configFile)
configFile.close()

URL = config['chili']['url']
API = config['chili']['api']
CUSTOMER_PROJECTS = config['chili']['customerProjects']
SYSFERA_PROJECTS = config['chili']['sysferaProjects']
SPRINT_TARGET = "%02d" % config['sprint']['end']['day'] + "-" + "%02d" % config['sprint']['end']['month'] + "-" + "%04d" % config['sprint']['end']['year']


def get_issues(issues, attr, field, value):
    issues_id = []
    for i in issues:
        if hasattr(i, attr):
            a = getattr(i, attr)
            if getattr(a, field) == value:
                issues_id.append(i.id)
    return issues.filter(issues_id)


def data(redmine):
    results = []

    issues = get_issues(redmine.issue.filter(status_id='1'), "fixed_version", "name", SPRINT_TARGET)
    for issue in issues:
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

if __name__ == '__main__':
    rmine = Redmine(URL, key=API, requests={'verify': False})
    tickets = data(rmine)
    for ticket in tickets:
        print "#" + str(ticket['number']) + " === OF: " + ticket['of'] + " === " + ticket['subject']