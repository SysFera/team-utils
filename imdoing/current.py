# ~*~ coding: utf-8 ~*~
from variables import *


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

    for a, b in my_dict.iteritems():
        string += getattr(TermColors, a) + b + TermColors.ENDC + " - "

    return string[:-3] + "\n"


def color_status(ticket):
    status = ticket['status']

    if status == 1:
        return TermColors.HEADER
    elif status == 2:
        return TermColors.WARNING
    elif status == 3:
        return TermColors.OKBLUE
    elif status == 5:
        return TermColors.OKGREEN
    elif status == 6:
        return TermColors.FAIL


def colorify(string, color):
    return color + string + TermColors.ENDC


def print_ticket(ticket, prefix=""):
    color = color_status(ticket)
    string = u"{}#{id} = {project:^7} = OF: {of} = " \
             u"{assignee:^10} = {subject}".format(prefix, **ticket)

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
        print u"No ticket found. Please check version_id " \
              u"is set correctly in config.json."


def data(status):
    results = []

    ids = REDMINE.issue.filter(status_id=status)
    issues = get_issues(ids, "fixed_version", "id", TARGET_VERSION)

    for issue in issues:
        issue_id = issue['id']

        if hasattr(issue, "parent"):
            parent_id = issue.parent.id
        else:
            parent_id = None

        cf_of = [cf['value'] for cf in issue['custom_fields']
                 if cf['name'] == "OF"][0]
        of = 'None' if cf_of == '' else str(cf_of)

        if hasattr(issue, "assigned_to"):
            assignee_id = getattr(issue, "assigned_to")['id']
            assignee = USERNAMES_REV[assignee_id]
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


def add_parser(subparsers):
    subparser = subparsers.add_parser('list',
                                      help='List tickets for the '
                                           'current sprint.')

    subparser.add_argument('status',
                           nargs='?',
                           help='the command arguments',
                           default='open',
                           choices=['open', 'all', 'closed'])


def run(args):
    status = "*" if args.status == "all" else args.status

    tickets = data(status)
    print_tree(tickets)