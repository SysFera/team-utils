# ~*~ coding: utf-8 ~*~
from variables import *


def add_parser(subparsers):
    now = datetime.now()
    week_now = now.isocalendar()[1]
    year_now = now.year

    subparser = subparsers.add_parser('fdt',
                                      help='Generates a csv output to be '
                                           'pasted in a FdT.')

    subparser.add_argument('user',
                           nargs='?',
                           default=CURRENT_USER,
                           type=str,
                           help='the user whom timesheet to display '
                                '(default: you)')

    subparser.add_argument('week',
                           nargs='?',
                           default=week_now,
                           type=int,
                           help='the week (default: current)')

    subparser.add_argument('year',
                           nargs='?',
                           default=year_now,
                           type=int,
                           help='the year (default: current)')


def add_entry(entries, date, of, hours, issue_id):
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
    user_id = USERNAMES[user]
    entries = {}

    # Filtering by user_id should work but does not,
    # so instead we'll download everything and then filter ourselves...
    # Yeah, it sucks.
    time_entries = REDMINE.time_entry.filter(**options)
    
    for entry in time_entries:
        # Currently, user_id filtering seems dead, so we need to
        # manually check for ownership
        if user_id == entry['user']['id']:
            issue_id = entry['issue']['id']
            issue = REDMINE.issue.get(issue_id)
            date = entry['spent_on']
            hours = entry['hours']
            of = ""

            if hasattr(issue, 'custom_fields'):
                fields = issue['custom_fields']
                of_list = [field['value'] for field in fields
                           if field['name'] == "OF"]
                if len(of_list) > 0:
                    of = str(of_list[0])

            add_entry(entries, date, of, hours, issue_id)
            total_hrs += hours

    return entries


def export_to_cvs(entries):
    delta_hrs = TARGET_HRS - total_hrs

    print "\nTimesheet for {} - Week n°{} - {}\n" \
          "Just copy-paste it in the FdT\n".format(user, week, year)

    if delta_hrs > 0:
        print "You need to declare {} hours more.\n".format(delta_hrs)
    elif delta_hrs < 0:
        print "You have declared {} hour(s) too much.\n".format(-delta_hrs)
    else:
        print "You have declared exactly {} hours. Cheater ;)\n" \
            .format(TARGET_HRS)

    print "{0:^4}|{1:^16}".format("OF", "Tickets"),
    print "|" * 22,
    days = ["Lu", "Ma", "Me", "Je", "Ve", "Sa"]
    for d in range(1, 7):
        print "{0:^3}".format(days[d-1]),
        print "" if d == 6 else "|",
    print ""
    print "=" * 79
    for of in sorted(entries.iterkeys()):
        issues = ", ".join(entries[of]['issues'])
        print "{0:>4}|{1:<16}".format(of, issues),
        print "|" * 22,

        for day in range(1, 7):
            obj = entries[of].get(day, {'hours': 0})
            hrs = obj['hours']
            hours = str(hrs).replace(".", ",") if not hrs == 0 else ""
            print "{0:>3}".format(hours),
            print "" if day == 6 else "|",
        print ""


def run(args):
    global user, week, year
    week = args.week
    year = args.year
    user = args.user

    start = iso_to_gregorian(year, week, 1)
    end = iso_to_gregorian(year, week, 6)

    options = {
        'from_date': start,
        'to_date': end,
        # Currently, it seems the API can return only 25 time entries at most.
        # To circumvent that we ask ChiliProject to send a page of 100 results.
        'per_page': 100
    }

    entries = get_entries(options)
    export_to_cvs(entries)