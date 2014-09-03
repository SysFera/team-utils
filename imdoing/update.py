# ~*~ coding: utf-8 ~*~
from variables import *


def process_notes(notes, options):
    do_update = False

    # we extract the notes since they behave differently than the rest
    if notes:
        do_update = True
        print u"\nIssue #{0} will have the following comment:\n{1}" \
            .format(options['ticket_id'], notes)
        prefix = "" if PERSONAL_KEY else "{0} :\n".format(CURRENT_USER)
        options['notes'] = "{0}{1}".format(prefix, notes)

    return do_update


def process_of(of, options, ticket):
    do_update = False

    if of:
        current_of = [cf['value'] for cf in ticket['custom_fields']
                      if cf['name'] == "OF"][0] or "None"
        of = unicode(str(of))
        if of == current_of:
            print u"\nIssue #{0} already has OF \"{1}\"; " \
                  u"OF will not be changed."\
                .format(options['ticket_id'], of)
        else:
            do_update = True
            print u"\nThe OF of issue #{0} will be changed to \"{1}\" from " \
                  u"\"{2}\".".format(options['ticket_id'], of, current_of)
            options['custom_fields'] = [{'id': 5, 'value': of}]

    return do_update


def check_already_assigned(properties):
    assigned_to = properties.get('assigned_to')
    user = assigned_to.get('user')['id']
    current = assigned_to.get('current')['id']

    # we return True (which means we need to --force) if
    # - user is not None
    #   a change of assigned_to was actually requested
    # - current != 0
    #   the ticket is already assigned to a real person (not 'nobody'/0)
    # - current != user
    #   the current user is not the requested user
    # - user != 0
    #   the requested user is not 'nobody' (if you typed --assigned_to nobody,
    #   you obviously want to de-assign the ticket from its current assignee)
    #
    # if all of the above evaluates to True, we return the current assignee
    return assigned_to.get('current')['label'] \
        if user is not None and current != 0 and current != user and user != 0\
        else ""


def build_properties(ticket, args):
    # we "pop" the ticket from the argument list.
    # any cleaner way of doing that is welcome!
    mod_args = {a: b for a, b in vars(args).iteritems()
                if a != 'ticket'
                and a != 'force'
                and a != 'of'
                and a != 'notes'
                and a != 'command'}

    # for each argument, we assign the dictionaries that will be used
    dicts = {
        'assigned_to': (USERNAMES, USERNAMES_REV),
        'status': (STATUSES, STATUSES_REV),
        'priority': (PRIORITIES, PRIORITIES_REV),
        'tracker': (TRACKERS, TRACKERS_REV)
    }

    # let's create the object we will return
    properties = {}

    # now, for each property in mod_args that is not None, we will create
    # an entry in our property object with all the info needed for the
    # update and for user feedback
    for prop, val in mod_args.iteritems():
        if hasattr(ticket, prop):
            ticket_prop_id = ticket[prop].id
        else:
            ticket_prop_id = 0

        user_label = dicts[prop][0][val] if val is not None else None
        current_label = dicts[prop][1][ticket_prop_id] if \
            ticket_prop_id is not None else None

        current_prop = {
            'name': prop,
            'code': prop + "_id",
            'user': {
                'id': user_label,
                'label': val
            },
            'current': {
                'id': ticket_prop_id,
                'label': current_label
            }
        }
        properties[prop] = current_prop

    return properties


def is_different(ticket_id, options, obj):
    if obj['user']['id'] is None:
        return False

    elif obj['user']['id'] == obj['current']['id']:
        print u"\nIssue #{0} already has {1} \"{2}\"; " \
              u"{1} will not be changed.".format(ticket_id, obj['name'],
                                                 obj['user']['label'])
        return False

    else:
        print u"\nThe {1} of issue #{0} will be changed to \"{2}\" from " \
              u"\"{3}\".".format(ticket_id, obj['name'], obj['user']['label'],
                                 obj['current']['label'])
        options[obj['code']] = obj['user']['id']
        return True


def update(**options):
    ticket_id = options.pop('ticket_id')

    # now that our option object is clean, we just submit the update
    if REDMINE.issue.update(ticket_id, **options):
        print u"\nIssue #{0} was successfully updated: " \
              u"https://support.sysfera.com/issues/{0}\n".format(ticket_id)
    else:
        print u"\nThere was an error updating issue #{0}\n".format(ticket_id)


def add_parser(subparsers):
    subparser = subparsers.add_parser('update',
                                      help='Updates a new ticket.')

    subparser.add_argument('ticket',
                           type=int,
                           help='the ticket number')

    subparser.add_argument('--assigned_to', '-a',
                           type=str,
                           choices=USERNAMES_L,
                           help='assign the ticket')

    subparser.add_argument('--status', '-s',
                           type=UNI,
                           choices=STATUSES_L,
                           help='the ticket\'s status')

    subparser.add_argument('--priority', '-p',
                           type=str,
                           choices=PRIORITIES_L,
                           help='the ticket\'s priority')

    subparser.add_argument('--tracker', '-t',
                           type=str,
                           choices=TRACKERS_L,
                           help='the ticket\'s tracker')

    subparser.add_argument('--of', '-o',
                           type=int,
                           help='the ticket\'s OF')

    subparser.add_argument('--force', '-f',
                           dest='force',
                           action='store_true',
                           default=False,
                           help='force the update')

    subparser.add_argument('--notes', '-n',
                           type=UNI,
                           help='any additional comment')


def run(args):
    # ticket_id will be used in several places
    ticket_id = args.ticket
    # we get the ticket from redmine
    ticket = REDMINE.issue.get(ticket_id)

    # we initialize the options object that we will use to update the ticket
    options = {'ticket_id': ticket_id}

    # we build a "complex" properties object that we will iterate through
    properties = build_properties(ticket, args)

    # was the command forced?
    if not args.force:
        # let's check if we won't require the user to --force their request
        already_assigned = check_already_assigned(properties)
        # did we get a name or did we get "" ?
        if already_assigned:
            # tell the user to run ith --force and exit
            print u"\nIssue #{0} was already assigned to {1}. Please run" \
                  u" again with -f if you want to force assign the issue.\n"\
                .format(ticket_id, already_assigned)
            sys.exit()

    # do_update is a flag that will be set to True if we actually need to
    # update the ticket
    # we process notes separately from the rest,
    # because the structure is different
    do_update = process_notes(args.notes, options)
    # likewise, we process the OF separately because it is a custom field
    do_update = process_of(args.of, options, ticket) or do_update

    # for each of the properties created, we check if we need to update
    # and populate "options" accordingly.
    for prop in properties.itervalues():
        # if at least one of the results is True, then do_update is True
        do_update = is_different(ticket_id, options, prop) or do_update

    if do_update:
        update(**options)