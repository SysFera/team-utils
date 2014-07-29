# ~*~ coding: utf-8 ~*~
from variables import *


def add_parser(subparsers):
    subparser = subparsers.add_parser('export',
                                      help='Exports all the time entries of '
                                           'a sprint.')


def add(entries, user, date, of, hours, issue_id):
    if not user in entries:
        entries[user] = {}
    if not date in entries[user]:
        entries[user][date] = {}
    if not of in entries[user][date]:
        entries[user][date][of] = {'hours': 0, 'issues': set()}

    entries[user][date][of]['hours'] += hours
    entries[user][date][of]['issues'].add(str(issue_id))


def get_entries(start, end):
    time_entries = REDMINE.time_entry.filter(from_date=start, to_date=end)
    entries = {}
    for entry in time_entries:
        issue_id = entry['issue']['id']
        issue = REDMINE.issue.get(issue_id)
        user = USERNAMES_REV[entry['user']['id']]
        date = entry['spent_on']
        hours = entry['hours']
        of = ""

        if hasattr(issue, 'custom_fields'):
            fields = issue['custom_fields']
            of_list = [field['value'] for field in fields
                       if field['name'] == "OF"]
            if len(of_list) > 0:
                of = str(of_list[0])

        add(entries, user, date, of, hours, issue_id)

    return entries


def export_to_csv(entries):
    filedir = os.path.join(TEAM_PATH, "export")
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    timestamp = u"{0.year}.{0.month:02}.{0.day:02}-" \
                u"{0.hour:02}:{0.minute:02}:{0.second:02}".format(NOW)
    filename = os.path.join(filedir, timestamp + '.csv')

    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['user', 'date', 'OF', 'hours', 'tickets'])

        for user in sorted(entries.iterkeys()):
            for date in sorted(entries[user].iterkeys()):
                for of in sorted(entries[user][date].iterkeys()):
                    hours = entries[user][date][of]['hours']
                    issues = ",".join(entries[user][date][of]['issues'])
                    writer.writerow([user, date, of, hours, issues])
                    print u"{0},{1},{2},{3},{4}"\
                        .format(user, date, of, hours, issues)


def run():
    start = datetime(SPRINT_START['year'], SPRINT_START['month'],
                     SPRINT_START['day'])
    end = datetime(SPRINT_END['year'], SPRINT_END['month'], SPRINT_END['day'])

    entries = get_entries(start, end)

    export_to_csv(entries)