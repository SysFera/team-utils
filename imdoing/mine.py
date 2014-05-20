# ! /usr/bin/python
# ~*~ coding: utf-8 ~*~

from redmine import Redmine
import json
import getpass
import argparse

configFile = open('config.json')
config = json.load(configFile)
configFile.close()

# non-standard modules required
# pip install python-redmine

URL = config['chili']['url']
API = config['chili']['api']
USERS = config['chili']['members']
USERNAMES = [str(U['name']) for U in USERS]
parser = argparse.ArgumentParser(description='List the tickets assigned to self or to $user.')
parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                    help='the user to whom tickets are assigned',
                    choices=USERNAMES)
args = parser.parse_args()
USER = args.user
USER_ID = [U['id'] for U in USERS if U['name'] == USER]


def data(redmine):
    results = []

    for issue in redmine.issue.filter(assigned_to_id=USER_ID):
        of = [cf['value'] for cf in issue['custom_fields'] if cf['name'] == "OF"][0]
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


if __name__ == '__main__':
    rmine = Redmine(URL, key=API, requests={'verify': False})
    tickets = data(rmine)

    print "Tickets assigned to user " + USER + ":"
    if len(tickets) > 0:
        for ticket in tickets:
            print "#" + str(ticket['number']) + " === OF: " + ticket['of'] + " === " + ticket['subject']
    else:
        print "No ticket found. Maybe you meant another user?"