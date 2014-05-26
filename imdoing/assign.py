# ~*~ coding: utf-8 ~*~

import getpass
import argparse


def get_assignee_id(rmine, ticket):
    issue = rmine.issue.get(ticket)

    if hasattr(issue, "assigned_to"):
        return getattr(issue, "assigned_to")['id']
    else:
        return 0


def assign(redmine, userid, ticket):
    status_id = 2  # Open
    ticket = redmine.issue.update(ticket, assigned_to_id=userid,
                                  status_id=status_id)
    return ticket


def run(rmine, arguments, users, usernames):
    parser = argparse.ArgumentParser(
        description='Assign a ticket to self or to $user.')
    parser.add_argument('ticket', type=int,
                        help='the ticket number')
    parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                        help='the user to whom tickets are assigned',
                        choices=usernames)
    parser.add_argument('-f', '--force', dest='forced', action='store_true', default=False)
    args = parser.parse_args(arguments)
    ticket = args.ticket
    user = args.user
    forced = args.forced

    userid = [U['id'] for U in users if U['name'] == user][0]
    assignee_id = get_assignee_id(rmine, ticket)
    assignee = [member['name'] for member in users if member['id'] == assignee_id][0]

    if assignee_id == userid:
        print u"Issue #{} was already assigned to {}. " \
              u"Nothing was done.".format(ticket, assignee)
    elif forced or assignee_id == 0:
        if assign(rmine, userid, ticket):
            print u"Issue #{} was successfully assigned to {}".format(ticket, user)
            print u"https://support.sysfera.com/issues/{}".format(ticket)
        else:
            print u"There was an error assigning issue #{} to {}".format(ticket, user)
    else:
        print u"Issue #{} was already assigned to {}. Please run again " \
              u"with -f if you want to force assign the issue." \
            .format(ticket, assignee)