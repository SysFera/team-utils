#!/usr/bin/python
# ~*~ coding: utf-8 ~*~
import getpass
import argparse

uni = lambda s: unicode(s, 'utf8')


def add_project_or_parent(args, options):
    project = args.project
    parent = args.parent
    parent_of = None

    # if project was not set (then parent was, by argparse construction)
    if project is None:
        # let's use the parent ticket's project
        parent_issue = options['redmine'].issue.get(parent)
        project = parent_issue['project']['id']
        # if the parent has an OF, we store it
        parent_of = [cf['value'] for cf in parent_issue['custom_fields']
                     if cf['name'] == "OF"][0]
    # "else" is implicit: because we use argparse, it means that:
    # project is set, parent is not set, there is no "default" OF

    # now we create the OF: either it was explicitly set, or it is inherited
    # from the parent, or it is None
    of = args.of or parent_of or ""

    options['custom_fields'] = [{'id': 5, 'value': str(of)}]
    options['parent_issue_id'] = parent
    options['project_id'] = project


def create(options):
    redmine = options.pop('redmine')

    # for k, v in options.iteritems():
    #     print k
    #     print v
    ticket = redmine.issue.create(**options)
    return ticket


def run(rmine, arguments, target, users, trackers, priorities, projects,
        statuses):
    project_list = sorted([project['name'] for project in projects])
    priorities_list = sorted([k for k in priorities.iterkeys()])
    trackers_list = sorted([k for k in trackers.iterkeys()])
    statuses_list = sorted([k for k in statuses.iterkeys()])
    usernames = {user['name']: user['id'] for user in users}
    usernames['nobody'] = 0
    users_list = sorted([k for k in usernames.iterkeys()])

    parser = argparse.ArgumentParser(description='Create a new ticket.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--parent', '-p', type=int)
    group.add_argument('--project', '-P', type=uni, choices=project_list)
    parser.add_argument('--subject', '-s', type=uni, required=True)
    parser.add_argument('--description', '-d', type=uni, required=True)
    parser.add_argument('--tracker', '-t', type=str, choices=trackers_list,
                        required=True)
    parser.add_argument('--priority', type=str, default='normal',
                        choices=priorities_list)
    parser.add_argument('--status', type=str, default='new',
                        choices=statuses_list)
    parser.add_argument('--assigned_to', type=uni, choices=users_list,
                        default='nobody')
    parser.add_argument('--of', type=int, default=0)
    args = parser.parse_args(arguments)

    options = {
        'redmine': rmine,
        'subject': args.subject,
        'priority_id': priorities[args.priority],
        'tracker_id': trackers[args.tracker],
        'description': args.description,
        'status_id': statuses[args.status],
        'fixed_version_id': target,
        'assigned_to_id': usernames[args.assigned_to]
    }

    add_project_or_parent(args, options)

    issue = create(options)
    if issue:
        print u"\nIssue #{0} was created by {1}: " \
              u"https://support.sysfera.com/issues/{0}\n"\
            .format(issue['id'], getpass.getuser())
    else:
        print u"There was an error. Please check the options and try again."