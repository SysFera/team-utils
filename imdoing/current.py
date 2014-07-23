# ~*~ coding: utf-8 ~*~
import argparse


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


def legend():
    string = "\n\nLegend: "
    my_dict = {
        "HEADER": "new",
        "OKBLUE": "solved",
        "OKGREEN": "closed",
        "WARNING": "open",
        "FAIL": "rejected"
    }

    for k, v in my_dict.iteritems():
        string += getattr(termColors, k) + v + termColors.ENDC + " - "

    return string[:-3] + "\n"


def color_status(ticket):
    status = ticket['status']

    if status == 1:
        return termColors.HEADER
    elif status == 2:
        return termColors.WARNING
    elif status == 3:
        return termColors.OKBLUE
    elif status == 5:
        return termColors.OKGREEN
    elif status == 6:
        return termColors.FAIL


def colorify(string, color):
    return color + string + termColors.ENDC


def print_ticket(ticket, prefix=""):
    color = color_status(ticket)
    string = prefix + u"#{id} = {project:^7} = OF: {of} = " \
                      u"{assignee:^10} = {subject}".format(**ticket)
    print colorify(string, color)
    children = ticket['children']
    if children:
        for child in children:
            new_prefix = "  " + prefix if prefix else "  \_ "
            print_ticket(child, new_prefix)


def print_tree(tickets):
    if len(tickets) > 0:
        print "\n"
        for result in tickets:
            print_ticket(result)
        print legend()
    else:
        print "No ticket found. Please check version_id " \
              "is set correctly in config.json."


def data(redmine, target, users, status):
    results = []

    issues = get_issues(redmine.issue.filter(status_id=status),
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
            'status': issue['status']['id'],
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


def parse():
    parser = argparse.ArgumentParser(
        description='list tickets for the current sprint.')
    parser.add_argument('current', type=str, help='the current sprint')
    parser.add_argument('status', nargs='?', help='the command arguments',
                        default='open', choices=['open', 'all', 'closed'])
    args = parser.parse_args()
    status = args.status

    return "*" if status == "all" else status


def run(rmine, target, users):
    args = parse()
    tickets = data(rmine, target, users, args)
    print_tree(tickets)