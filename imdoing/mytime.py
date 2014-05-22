#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

from datetime import datetime
import os
import dateutil.parser
import json
import getpass
import getopt
import sys



NOW = datetime.now()
DATE = "%(Y)d.%(m)02d.%(d)02d-%(H)02d:%(M)02d:%(S)02d" % {"Y": NOW.year, "m": NOW.month, "d": NOW.day,
                                                          "H": NOW.hour, "M": NOW.minute, "S": NOW.second}


def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_log(directory, date, user, ticket, action):
    basename = '%(date)s-%(user)s-%(ticket)d-%(action)s' % {"directory": directory, "date": date, "user": user,
                                                            "ticket": ticket, "action": action}
    filename = os.path.join(directory, basename)

    if not os.path.isfile(filename):
        try:
            open(filename, 'w').close()
            print '%(user)s %(action)ss working on ticket #%(ticket)d' % {"user": user, "action": action, "ticket": ticket}
        except IOError, e:
            print 'There was an error starting the log.'
            print e
    else:
        print "The file already exists. As this is highly unlikely, something bad is probably going on ;)"


def run(arguments, users, direc, action):
    userid = ""
    user = getpass.getuser()
    ticket = ""
    try:
        opts, args = getopt.getopt(arguments, "u:", "user")
    except getopt.GetoptError:
        print 'Error checking options for mine'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--user"):
            user = arg
    for arg in args:
        try:
            ticket = int(args[0])
        except:
            print "Invalid ticket number"
            sys.exit(2)
    userid = [U['id'] for U in users if U['name'] == user]


    if ticket == "" or userid == "":
        print "Missing parameter"
        print "Usage: imdoing start/stop [-u username]  <ticket_number>"
        sys.exit(2)


    directory = os.path.join(direc, "timelog", user)
    check_dir(directory)
    write_log(directory, DATE, user, ticket, action)

