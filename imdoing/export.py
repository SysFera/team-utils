# ~*~ coding: utf-8 ~*~
from variables import *


def add_parser(subparsers):
    subparser = subparsers.add_parser('export',
                                      help='Generates a csv output of time'
                                           'entries between two dates.')

    subparser.add_argument('date_from',
                           type=str,
                           help='the from date (string, "YYYYMMDD")')

    subparser.add_argument('date_to',
                           type=str,
                           help='the to date (string, "YYYYMMDD")')


def get_of():
    filedir = os.path.join(TEAM_PATH, "consolidate", "data")
    filename = os.path.join(filedir, 'OF.csv')

    ofs = {}

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            ofs[unicode(row[0], 'utf8')] = unicode(row[1], 'utf8')

    return ofs


def get_nre():
    filedir = os.path.join(TEAM_PATH, "consolidate", "data")
    filename = os.path.join(filedir, 'OF.csv')

    nres = {}

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            nres[unicode(row[0], 'utf8')] = unicode(row[3], 'utf8') or "N/A"

    return nres


def get_entries():
    entries = []
    # Since we are limited by ChiliProject to 100 time entries at a time,
    # we will need to query for each day instead of day per day.
    d = date_from
    delta = timedelta(days=1)
    while d <= date_to:
        day = "{0.year}{0.month:0>2}{0.day:0>2}".format(d)
        daily_entries = REDMINE.time_entry.filter(from_date=day, to_date=day,
                                                  per_page=100)

        for daily_entry in daily_entries:
            entry = {
                "id": daily_entry['id'],
                "date": daily_entry['spent_on'],
                "ticket": daily_entry['issue']['id'],
                "title": "N/A",
                "project": daily_entry['project']['name'],
                "comments": "N/A",
                "user": USERNAMES_REV[daily_entry['user']['id']],
                "of": "N/A",
                "of_name": "N/A",
                "nre": "N/A",
                "time": daily_entry['hours']
            }

            if hasattr(daily_entry, 'comments'):
                entry['comments'] = getattr(daily_entry, 'comments')\
                    .replace('"', '""')

            issue_id = daily_entry['issue']['id']
            issue = REDMINE.issue.get(issue_id)
            entry['title'] = issue['subject'].replace('"', '""')

            if hasattr(issue, 'custom_fields'):
                fields = issue['custom_fields']
                of_list = [field['value'] for field in fields
                           if field['name'] == "OF"]
                try:
                    if len(of_list) > 0:
                        entry['of'] = str(of_list[0])
                        entry['of_name'] = list_of[entry['of']]
                        entry['nre'] = list_nre[entry['of']]
                except KeyError:
                    print entry['title'] + " - " + \
                        "https://support.sysfera.com/issues/" + \
                        str(entry['ticket'])

            entries.append(entry)

        d += delta

    return entries


def export_to_cvs(entries):
    filedir = os.path.join(TEAM_PATH, "export")
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    timestamp = u"{0.year}.{0.month:02}.{0.day:02}-" \
                u"{0.hour:02}:{0.minute:02}:{0.second:02}".format(NOW)
    filename = os.path.join(filedir, timestamp + '.csv')

    with open(filename, 'wb') as f:
        header = u"id,date,ticket,title,project,comments,user," \
                 u"of,of_name,nre,time"
        f.write(header.encode('utf8'))
        for entry in entries:
            line = u"\n{id},{date},{ticket},\"{title}\",{project}," \
                   u"\"{comments}\",{user},{of},{of_name},{nre},{time}"\
                .format(**entry)
            f.write(line.encode('utf8'))


def run(args):
    global date_from, date_to, list_of, list_nre

    list_of = get_of()
    list_nre = get_nre()

    date_from = datetime.strptime(args.date_from, "%Y%m%d").date()
    date_to = datetime.strptime(args.date_to, "%Y%m%d").date()

    entries = get_entries()
    export_to_cvs(entries)