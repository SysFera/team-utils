# ~*~ coding: utf-8 ~*~


def get_issues(issues, attr, field, value):
    issues_id = []
    for i in issues:
        if hasattr(i, attr):
            a = getattr(i, attr)
            if getattr(a, field) == value:
                issues_id.append(i.id)
    return issues.filter(issues_id)


def data(redmine, target, users):
    results = []

    issues = get_issues(redmine.issue.filter(status_id='1'),
                        "fixed_version", "id", target)
    for issue in issues:
        of = [cf['value'] for cf in issue['custom_fields']
              if cf['name'] == "OF"][0]
        if of == '':
            of = "None"
        else:
            of = str(of)

        if hasattr(issue, "assigned_to"):
            assignee_id = getattr(issue, "assigned_to")['id']
            assignee = [user['name'] for user in users if user['id'] == assignee_id][0]
        else:
            assignee = "unassigned"

        result = {
            'number': issue['id'],
            'subject': issue['subject'],
            'assignee': assignee,
            'of': of
        }
        results.append(result)

    return results


def run(rmine, target, users):
    tickets = data(rmine, target, users)
    if len(tickets) > 0:
        for ticket in tickets:
            print u"#{number} === OF: {of} == {assignee:^10} == {subject}".format(**ticket)
    else:
        print "No ticket found. Please check version_id is set correctly in config.json."
