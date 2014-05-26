#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

# non-standard modules required
# pip install python-redmine
import os

from redmine import Redmine
import json


def get_issues(issues, attr, field, value):
    issues_id = []
    for i in issues:
        if hasattr(i, attr):
            a = getattr(i, attr)
            if getattr(a, field) == value:
                issues_id.append(i.id)
    return issues.filter(issues_id)


def data(redmine, target):
    results = []

    issues = get_issues(redmine.issue.filter(status_id='1'),
                        "fixed_version", "name", target)
    for issue in issues:
        of = [cf['value'] for cf in issue['custom_fields']
              if cf['name'] == "OF"][0]
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


def run(rmine, arguments, target):
    tickets = data(rmine, target)
    for ticket in tickets:
        print "#{number} === OF: {of} === {subject}".format(**ticket)

