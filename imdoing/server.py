#!/usr/bin/env python
import web
import json
import shelve
import os
import sys

urls = (
    '/register', 'Register',
    '/timelog/(.+)', 'User'
)


def get_dir():
    directory = os.environ.get('TEAM_PATH')
    if directory is not None:
        return os.path.join(directory, "imdoing")
    print "The environment variable TEAM_PATH is not set. Aborting."
    sys.exit()

configFile = open(os.path.join(get_dir(), os.pardir,
                               'dashboard', 'data',
                               'config.json'))
config = json.load(configFile)
configFile.close()
USERS = config['chili']['members']

app = web.application(urls, globals())


class User:
    def GET(self, user):
        if user not in [U['name'] for U in USERS]:
            out = 'Possible members are:'
            for i, U in enumerate(USERS):
                out += ' {}'.format(U['name'])
                if i < len(USERS):
                    out += ','

        else:
            s = shelve.open(user + '.db')
            out = u'Tickets for {}:\n\n'.format(user)

            if s == {}:
                out += u'No timelog found.'
            else:
                for date, log in s.iteritems():
                    out += u'{} === {} - {}\n'.format(date, log['ticket'], log['action'])

        return out


class Register:
    def GET(self):
        return 'Use POST, stupid.'

    def POST(self):
        print "Received POST data"
        data = json.loads(web.data())
        date = str(data['date'])
        user = data['user']

        # opens the user's db
        s = shelve.open(user + '.db')

        try:
            existing = s[date]
        except KeyError:
            try:
                s[date] = {
                    'ticket': data['ticket'],
                    'action': data['action']
                }
            except KeyError:
                web.ctx.status = "500 Internal Server Error"
                return "An error occurred in the database."
            else:
                return u'{user} {action}s working on ticket {ticket} at {date} (registered on the server)'.format(**data)
        else:
            web.ctx.status = "500 Internal Server Error"
            return "A log already exists for {user} at {date}".format(**data)


if __name__ == "__main__":
    app.run()