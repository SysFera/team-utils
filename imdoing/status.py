# ~*~ coding: utf-8 ~*~

import argparse


def run(arguments, statuses):
    parser = argparse.ArgumentParser(description=
                                     'Changes the status of a ticket. '
                                     'DEPECRATED: use imdoing update')
    parser.add_argument('ticket', type=int, help='the ticket\'s number')
    parser.add_argument('status', type=str, help='the ticket\'s status',
                        choices=statuses)
    args = parser.parse_args(arguments)
    ticket = args.ticket
    status = args.status

    print "DEPECRATED. Please use:"
    print "imdoing update {0} --status {1}".format(ticket, status)