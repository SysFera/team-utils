# ~*~ coding: utf-8 ~*~

import getpass
import argparse


def run(arguments, usernames):
    parser = argparse.ArgumentParser(
        description='Assign a ticket to self or to $user. '
                    'DEPECRATED: use imdoing update.')
    parser.add_argument('ticket', type=int, help='the ticket\'s number')
    parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                        help='the user to assign the ticket to',
                        choices=usernames+["nobody"])
    parser.add_argument('-f', '--force', dest='forced', action='store_true',
                        default=False)
    args = parser.parse_args(arguments)
    force = " -f" if args.forced else ""
    user = args.user
    ticket = args.ticket

    print "DEPECRATED. Please use:"
    print "imdoing update{0} {1} --assigned_to {2}".format(force, ticket, user)