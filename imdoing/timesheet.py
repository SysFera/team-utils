# ~*~ coding: utf-8 ~*~
import argparse
import getpass
import datetime
from isocalendar_utils import iso_to_gregorian


def add(entries, date, of, hours, issue_id):
    isocalendar = date.isocalendar()
    day = isocalendar[2]

    if not of in entries:
        entries[of] = {'issues': set()}
    if not day in entries[of]:
        entries[of][day] = {'hours': 0}

    entries[of][day]['hours'] += hours
    entries[of]['issues'].add(str(issue_id))


def get_entries(options):
    global total_hrs
    total_hrs = 0
    redmine = options.pop('rmine')
    user_id = options.pop("user_id")
    entries = {}

    # filtering by user_id should work but does not,
    # so instead we'll download everything and then filter ourselves...
    # yeah, it sucks.
    time_entries = redmine.time_entry.filter(**options)

    for entry in time_entries:
        if user_id == entry['user']['id']:
            issue_id = entry['issue']['id']
            issue = redmine.issue.get(issue_id)
            date = entry['spent_on']
            hours = entry['hours']
            of = ""

            if hasattr(issue, 'custom_fields'):
                fields = issue['custom_fields']
                of_list = [field['value'] for field in fields
                           if field['name'] == "OF"]
                if len(of_list) > 0:
                    of = str(of_list[0])

            add(entries, date, of, hours, issue_id)
            total_hrs += hours

    return entries


def export_to_cvs(entries):
    delta_hrs = target_hrs - total_hrs

    print "\nTimesheet for {} - Week n°{} - {}\n" \
          "Just copy-paste it in the FdT\n".format(user, week, year)

    if delta_hrs > 0:
        print "You need to declare {} hours more.\n".format(delta_hrs)
    elif delta_hrs < 0:
        print "You have declared {} hour(s) too much.\n".format(-delta_hrs)
    else:
        print "You have declared exactly {} hours. Cheater ;)\n"\
            .format(target_hrs)

    for of in sorted(entries.iterkeys()):
        issues = ", ".join(entries[of]['issues'])
        print "{0}\t{1}".format(of, issues),
        print "\t" * 21,

        for day in range(1, 7):
            obj = entries[of].get(day, {'hours': 0})
            hrs = obj['hours']
            hours = str(hrs).replace(".", ",") if not hrs == 0 else ""
            print "\t{0}".format(hours),
        print ""


def parse_args(arguments):
    now = datetime.datetime.now()

    parser = argparse.ArgumentParser(
        description='prints a csv output for the given week, ready to'
                    'paste in the FdT.')
    parser.add_argument('user', nargs='?', default=getpass.getuser(), type=str,
                        help='the user to whom tickets are assigned',
                        choices=usernames)
    parser.add_argument('week', type=int, help='the week')
    parser.add_argument('year', nargs='?', default=now.year, type=int,
                        help='the year')

    return parser.parse_args(arguments)


def run(rmine, arguments, users):
    global usernames, usernames_rev, user, week, year, target_hrs
    target_hrs = 38.5

    # we create a mapping [username: id]
    usernames = {user['name']: user['id'] for user in users}
    usernames_rev = {v: k for k, v in usernames.iteritems()}

    args = parse_args(arguments)

    week = args.week
    year = args.year
    user = args.user

    start = iso_to_gregorian(year, week, 1)
    end = iso_to_gregorian(year, week, 6)

    options = {
        'rmine': rmine,
        'user_id': usernames[user],
        'from_date': start,
        'to_date': end
    }

    entries = get_entries(options)

    export_to_cvs(entries)