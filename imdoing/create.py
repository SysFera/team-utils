# ~*~ coding: utf-8 ~*~
from variables import *


def add_project_or_parent(options):
    project = options.pop('project')
    parent = options.pop('parent')
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
    of = options.pop('of') or parent_of or ""

    options['custom_fields'] = [{'id': 5, 'value': str(of)}]
    options['parent_issue_id'] = parent
    options['project_id'] = project


def create(options):
    issue = REDMINE.issue.create(**options)

    if issue:
        print u"\nIssue #{0} was created by {1}: " \
              u"https://support.sysfera.com/issues/{0}\n" \
            .format(issue['id'], CURRENT_USER)
    else:
        print u"There was an error. Please check the options and try again."


def add_parser(subparsers):
    subparser = subparsers.add_parser('export',
                                      help='Create a new ticket.')
    group = subparser.add_mutually_exclusive_group(required=True)
    group.add_argument('--parent', '-p',
                       type=int)
    group.add_argument('--project', '-P',
                       type=UNI,
                       choices=PROJECTS_L)

    subparser.add_argument('--subject', '-s',
                           type=UNI,
                           required=True)

    subparser.add_argument('--description', '-d',
                           type=UNI,
                           required=True)

    subparser.add_argument('--tracker', '-t',
                           type=str,
                           choices=TRACKERS_L,
                           required=True)

    subparser.add_argument('--priority',
                           type=str,
                           choices=PRIORITIES_L,
                           default='normal')

    subparser.add_argument('--status',
                           type=str,
                           choices=STATUSES_L,
                           default='new')

    subparser.add_argument('--assigned_to',
                           type=UNI,
                           choices=USERNAMES_L,
                           default='nobody')

    subparser.add_argument('--of',
                           type=int,
                           default=0)


def run(args):

    options = {
        'parent': args.parent,
        'project': args.project,
        'subject': args.subject,
        'of': args.of,
        'priority_id': PRIORITIES[args.priority],
        'tracker_id': TRACKERS[args.tracker],
        'description': args.description,
        'status_id': STATUSES[args.status],
        'fixed_version_id': TARGET_VERSION,
        'assigned_to_id': USERNAMES[args.assigned_to]
    }

    add_project_or_parent(options)

    create(options)