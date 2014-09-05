# ~*~ coding: utf-8 ~*~
from variables import *


def get_issues(issues, attr, field, value, recurrent):
    issues_id = []
    for i in issues:
        if hasattr(i, attr):
            a = getattr(i, attr)
            if getattr(a, field) == value:
                issues_id.append(i.id)
            elif recurrent and getattr(a, field) == RECURRENT_TARGET:
                issues_id.append(i.id)

    return issues.filter(issues_id)


def convert_to_int_status(limit):
        if limit == "new":
            return 1
        elif limit == "open":
            return 2
        elif limit == "solved":
            return 3
        elif limit == "closed":
            return 5
        elif limit == "rejected":
            return 6


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


def sort_status(tickets):
    closed = []
    new = []
    solved = []
    rejected = []
    opened = []
    for ticket in tickets:
        status = ticket['status']
        if status == 1:
            new.append(ticket)
        elif status == 2:
            opened.append(ticket)
        elif status == 3:
            solved.append(ticket)
        elif status == 5:
            closed.append(ticket)
        elif status == 6:
            rejected.append(ticket)

    return closed + rejected + solved + new + opened


def print_sort_status(tickets):
    if len(tickets) > 0:
        print "\n"
        for result in tickets:
            print_single_ticket(result)
        print legend()
    else:
        print u"No ticket found. Please check version_id " \
              u"is set correctly in config.json."


def print_tickets(tickets, sort):
    if sort == "status":
        sorted_list = sort_status(tickets)
        print_sort_status(sorted_list)
    else:
        print_tree(tickets)


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


def print_single_ticket(ticket, prefix=""):
    color = color_status(ticket)
    string = u"{}#{id} = {project:^7} = OF: {of} = " \
             u"{assignee:^10} = {subject}".format(prefix, **ticket)

    print colorify(string, color)


def print_tree(tickets):
    if len(tickets) > 0:
        print "\n"
        for result in tickets:
            print_ticket(result)
        print legend()
    else:
        print u"No ticket found. Please check version_id " \
              u"is set correctly in config.json."


def data(status, recurrent, sort, project, luke, limit):
    results = []

    ids = REDMINE.issue.filter(status_id=status)
    issues = get_issues(ids, "fixed_version", "id", TARGET_VERSION, recurrent)

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

        lnr = (limit is None) or (limit == result['status'])
        pnr = (project is None) or (project == result['project'])

        if pnr and lnr:
            results.append(result)

    if sort == 'tree':
        for result in results:
            for child in results:
                if child['parent_id'] is not None:
                    if child['parent_id'] == result['id']:
                        result['children'].append(child)
        if luke is None:
            results = [x for x in results if not x['parent_id']]
        else:
            son = [x for x in results if x['id'] == int(luke)]
            if son:
                darthvader = son[0]
            else:
                return []
            while darthvader['parent_id'] is not None:
                son = [x for x in results
                       if x['id'] == darthvader['parent_id']]
                darthvader = son[0]
            results = [darthvader]

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

    subparser.add_argument("--rec", "-r",
                           help="display including recurrent target tickets",
                           action="store_true")

    subparser.add_argument("--sort", "-s",
                           help="sort the tickets by status",
                           default='date',
                           choices=['tree', 'status', 'date'])

    subparser.add_argument("--project", "-p",
                           help="show the tickets corresponding to the "
                                "specified project")

    subparser.add_argument("--limit", "-l",
                           help="show the tickets limited to the given status",
                           default='all',
                           choices=['all', 'open', 'closed', 'solved',
                                    'new', 'rejected'])

    subparser.add_argument("--family", "-f",
                           help="show the tickets in the same family as "
                                "that one (parents and children). Need the "
                                "tree sort option to work.")


def run(args):
    status = "*" if args.status == "all" else args.status
    recurrent = args.rec
    sort = args.sort
    project = args.project
    family = args.family
    limit = convert_to_int_status(args.limit)

    tickets = data(status, recurrent, sort, project, family, limit)

    print_tickets(tickets, sort)
