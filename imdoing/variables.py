# ~*~ coding: utf-8 ~*~
from redmine import Redmine
from datetime import datetime
from datetime import timedelta
import os
import json
import sys
import getpass
import csv
from isocalendar_utils import iso_to_gregorian


class TermColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def get_dir():
    directory = os.environ.get('TEAM_PATH')

    if not directory:
        print "The environment variable TEAM_PATH is not set. Aborting."
        sys.exit()

    return os.path.join(directory, "imdoing")


def get_api_key():
    api_key = os.environ.get('CHILI_API_KEY')

    if api_key is None:
        print """
Sorry, the CHILI_API_KEY environment variable was not set, you cannot \
use the time-tracking features.
To generate the key, please use the link in the left column at
https://support.sysfera.com/my/account
and add the following to your .bashrc (or something):
export CHILI_API_KEY=XXX
"""

    return api_key


CURRENT_USER = getpass.getuser()

UNI = lambda s: unicode(s, 'utf8')

NOW = datetime.now()
DATE = u"{0.year}-{0.month:02}-{0.day:02}".format(NOW)

TEAM_PATH = get_dir()
configFile = open(os.path.join(TEAM_PATH, os.pardir,
                               'dashboard', 'data',
                               'config.json'))
config = json.load(configFile)
configFile.close()

USERS = config['chili']['members']
USERNAMES = {USER['name']: USER['id'] for USER in USERS}
USERNAMES['nobody'] = 0
USERNAMES_REV = {v: k for k, v in USERNAMES.iteritems()}
USERNAMES_L = sorted([k for k in USERNAMES.iterkeys()])

CUSTOMER_PROJECTS = config['chili']['customerProjects']
SYSFERA_PROJECTS = config['chili']['sysferaProjects']
PROJECTS = CUSTOMER_PROJECTS + SYSFERA_PROJECTS
PROJECTS_L = sorted([PROJECT['name'] for PROJECT in PROJECTS])

TRACKERS = config['chili']['trackers']
TRACKERS_REV = {v: k for k, v in TRACKERS.iteritems()}
TRACKERS_L = sorted([k for k in TRACKERS.iterkeys()])

STATUSES = config['chili']['statuses']
STATUSES_REV = {v: k for k, v in STATUSES.iteritems()}
STATUSES_L = sorted([k for k in STATUSES.iterkeys()])

PRIORITIES = config['chili']['priorities']
PRIORITIES_REV = {v: k for k, v in PRIORITIES.iteritems()}
PRIORITIES_L = sorted([k for k in PRIORITIES.iterkeys()])

TARGET_VERSION = config['chili']['version_id']
SPRINT_START = config['sprint']['start']
SPRINT_END = config['sprint']['end']

URL = config['chili']['url']
COMMON_KEY = config['chili']['api']
PERSONAL_KEY = get_api_key()
API_KEY = PERSONAL_KEY if PERSONAL_KEY else COMMON_KEY
REDMINE = Redmine(URL, key=API_KEY, requests={'verify': False})

TARGET_HRS = 38.5
RECURRENT_TARGET=20
