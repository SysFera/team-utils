#!/usr/bin/env python
import web
import json

urls = (
    '/register', 'Register'
)

app = web.application(urls, globals())


class Register:
    def GET(self):
        return 'Use POST, stupid.'

    def POST(self):
        print "Received POST data"
        data = json.loads(web.data())

        # web.ctx.status can be used to change the HTTP status code if server registration fails.
        # web.ctx.status = "200 OK"
        # web.ctx.status = "500 Internal Server Error"

        return u'{user} {action}s working on ticket {ticket} at {date} (registered on the server)'.format(**data)


if __name__ == "__main__":
    app.run()