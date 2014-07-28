# ~*~ coding: utf-8 ~*~
from datetime import datetime
from xlrd import open_workbook
from xlutils.copy import copy
import xlwt
import os


def add(entries, user, date, of, hours, issue_id):
    isocalendar = date.isocalendar()
    week = isocalendar[1]
    day = isocalendar[2]

    if not user in entries:
        entries[user] = {}
    if not week in entries[user]:
        entries[user][week] = {}
    if not of in entries[user][week]:
        entries[user][week][of] = {'issues': set()}
    if not day in entries[user][week][of]:
        entries[user][week][of][day] = {'hours': 0}

    entries[user][week][of][day]['hours'] += hours
    entries[user][week][of]['issues'].add(str(issue_id))


def get_entries(start, end):
    time_entries = redmine.time_entry.filter(from_date=start, to_date=end)
    entries = {}
    for entry in time_entries:
        issue_id = entry['issue']['id']
        issue = redmine.issue.get(issue_id)
        user = usernames_rev[entry['user']['id']]
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


def get_xls(user):
    filepath = os.path.join(path, "FdT", user + ".xls")
    new_filepath = os.path.join(path, "FdT", user + "-modified.xls")
    book = open_workbook(filepath, formatting_info=True, on_demand=True)
    new_book = copy(book)

    return new_book


def export_to_xls(entries):
    for user in sorted(entries.iterkeys()):
        if user == "aragon":
            new_filepath = os.path.join(path, "FdT", user + "-modified.xls")
            new_book = get_xls(user)
            print "Timesheet for {}".format(user)
            for week in sorted(entries[user].iterkeys()):
                sheet = new_book.get_sheet(week + 2)
                row = 5
                print "Week n°{}".format(week)
                print "{0:<6}{1:<20}{2:<6}{3:<6}{4:<6}{5:<6}{6:<6}{7:<6}"\
                    .format("OF", "Tickets", "Lu", "Ma", "Me", "Je", "Ve", "Sa")
                for of in sorted(entries[user][week].iterkeys()):
                    issues = ",".join(entries[user][week][of]['issues'])
                    col = 0
                    sheet.write(row, col, of)
                    col = 1
                    sheet.write(row, col, issues)
                    col = 23

                    print "{0:<6}{1:<20}".format(of, issues),

                    for day in range(1, 7):
                        obj = entries[user][week][of].get(day, {'hours': 0})
                        hours = obj['hours']

                        sheet.write(row, col, hours)
                        col += 1

                        print "{0:<6}".format(str(hours)),

                    row += 1

                    print "\n"

            new_book.save(new_filepath)


def run(rmine, sprint_start, sprint_end, users, team_path):
    global redmine, usernames, usernames_rev, filedir, path

    path = team_path
    filedir = os.path.join(team_path, "export")
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    # we create a mapping [username: id]
    usernames = {user['login']: user['id'] for user in users}
    usernames_rev = {v: k for k, v in usernames.iteritems()}

    redmine = rmine

    start = datetime(sprint_start['year'], sprint_start['month'],
                     sprint_start['day'])
    end = datetime(sprint_end['year'], sprint_end['month'], sprint_end['day'])

    entries = get_entries(start, end)

    export_to_xls(entries)