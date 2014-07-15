# ~*~ coding: utf-8 ~*~


class termColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def get_issues(issues, attr, field, value):
    issues_id = []
    for i in issues:
        if hasattr(i, attr):
            a = getattr(i, attr)
            if getattr(a, field) == value:
                issues_id.append(i.id)
    return issues.filter(issues_id)


def print_ticket(result, prefix=""):
    if not result["parent_id"]:
        start = termColors.OKBLUE
        end = termColors.ENDC
    else:
        start = termColors.WARNING
        end = termColors.ENDC

    print start + prefix + u"#{id} = {project:^7} = OF: {of} = {assignee:^10} = {subject}".format(**result) + end
    children = result['children']
    if children:
        for child in children:
            new_prefix = "  " + prefix if prefix else "  \_ "
            print_ticket(child, new_prefix)


def print_tree(results):
    if len(results) > 0:
        for result in results:
            print_ticket(result)
    else:
        print "No ticket found. Please check version_id is set correctly in config.json."


def data(redmine, target, users):
    results = []

    issues = get_issues(redmine.issue.filter(status_id='open'),
                        "fixed_version", "id", target)

    for issue in issues:
        issue_id = issue['id']

        if hasattr(issue, "parent"):
            parent_id = issue.parent.id
        else:
            parent_id = None

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
            'id': issue_id,
            'subject': issue['subject'],
            'assignee': assignee,
            'of': of,
            'project': issue['project']['name'],
            'parent_id': parent_id,
            'children': []
        }
        results.append(result)

    for result in results:
        for child in results:
            if child['parent_id'] is not None:
                if child['parent_id'] == result['id']:
                    result['children'].append(child)

    results = [x for x in results if not x['parent_id']]

    return results


def run(rmine, target, users):
    tickets = data(rmine, target, users)
    print_tree(tickets)