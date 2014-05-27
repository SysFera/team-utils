# ~*~ coding: utf-8 ~*~

import getpass
import argparse


def get_status_id(rmine, ticket):
    issue = rmine.issue.get(ticket)

    # returns the issue's status id if it has one, 0 if not
    if hasattr(issue, "status"):
        return getattr(issue, "status")['id']
    else:
        return 0


def change_status(redmine, target_id, ticket):
    ticket = redmine.issue.update(ticket, status_id=target_id)

    return ticket


def run(rmine, arguments, statuses):
    parser = argparse.ArgumentParser(description='Changes the status of a ticket.')
    parser.add_argument('ticket', type=int, help='the ticket number')
    parser.add_argument('status', type=str, help='the ticket status', choices=statuses)
    args = parser.parse_args(arguments)
    ticket = args.ticket
    target = args.status
    target_id = statuses[target]

    status_id = get_status_id(rmine, ticket)

    if status_id == target_id:
        print u"Issue #{} already has status {}. " \
              u"Nothing was done.".format(ticket, target)
    else:
        if change_status(rmine, target_id, ticket):
            print u"Issue #{} was successfully changed to status {}".format(ticket, target)
            print u"https://support.sysfera.com/issues/{}".format(ticket)
        else:
            print u"There was an error changing the statue of issue #{} to {}".format(ticket, target)