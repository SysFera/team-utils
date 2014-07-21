# ~*~ coding: utf-8 ~*~

import argparse


def build_properties(ticket, args, usernames, statuses, priorities, trackers):
    # we "pop" the ticket from the argument list.
    # any cleaner way of doing that is welcome!
    mod_args = {k: v for k, v in vars(args).iteritems() if k != 'ticket'}

    # we create reverse dictionaries for easy lookup
    usernames_rev = {v: k for k, v in usernames.iteritems()}
    statuses_rev = {v: k for k, v in statuses.iteritems()}
    priorities_rev = {v: k for k, v in priorities.iteritems()}
    trackers_rev = {v: k for k, v in trackers.iteritems()}

    # for each argument, we assign the dictionaries that will be used
    dicts = {
        'assigned_to': (usernames, usernames_rev),
        'status': (statuses, statuses_rev),
        'priority': (priorities, priorities_rev),
        'tracker': (trackers, trackers_rev)
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

        current_prop = {
            'name': prop,
            'code': prop + "_id",
            'user': {
                'id': dicts[prop][0][val] if val is not None else None,
                'label': val
            },
            'current': {
                'id': ticket_prop_id,
                'label': dicts[prop][1][ticket_prop_id] if ticket_prop_id is not None else None
            }
        }
        properties[prop] = current_prop

    return properties


def is_different(ticket_id, options, obj):
    if obj['user']['id'] is None:
        return False

    elif obj['user']['id'] == obj['current']['id']:
        print u"Issue #{0} already has {1} \"{2}\"; " \
              u"{1} will not be changed.".format(ticket_id, obj['name'],
                                                 obj['user']['label'])
        return False

    else:
        print u"The {1} of issue #{0} will be changed to \"{2}\" from " \
              u"\"{3}\".".format(ticket_id, obj['name'], obj['user']['label'],
                                 obj['current']['label'])
        options[obj['code']] = obj['user']['id']
        return True


def update(**options):
    # we remove the rmine and ticket options
    rmine = options.pop('rmine')
    ticket_id = options.pop('ticket_id')

    # now that our option object is clean, we just submit the update
    if rmine.issue.update(ticket_id, **options):
        print u"Issue #{} was successfully updated".format(ticket_id)
    else:
        print u"There was an error updating issue #{}".format(ticket_id)


def run(rmine, arguments, users, statuses, priorities, trackers):
    # we create a mapping [username: id]
    usernames = {user['name']: user['id'] for user in users}
    usernames['nobody'] = 0

    # we create sorted lists for options
    usernames_s = sorted([username for username in usernames.iterkeys()])
    statuses_s = sorted([status for status in statuses.iterkeys()])
    priorities_s = sorted([priority for priority in priorities.iterkeys()])
    trackers_s = sorted([tracker for tracker in trackers.iterkeys()])

    # we create the parser
    parser = argparse.ArgumentParser(description='Updates a ticket.')
    parser.add_argument('ticket', type=int, help='the ticket number')
    parser.add_argument('--assigned_to', '-a', type=str,
                        help='assign the ticket', choices=usernames_s)
    parser.add_argument('--status', '-s', type=str,
                        help='the ticket\'s status', choices=statuses_s)
    parser.add_argument('--priority', '-p', type=str,
                        help='the ticket\'s priority',
                        choices=priorities_s)
    parser.add_argument('--tracker', '-t', type=str,
                        help='the ticket\'s tracker', choices=trackers_s)
    args = parser.parse_args(arguments)

    # ticket_id will be used in several places
    ticket_id = args.ticket

    # we get the ticket from redmine
    ticket = rmine.issue.get(ticket_id)

    # we build a "complex" properties object that we will iterate through
    properties = build_properties(ticket, args, usernames, statuses,
                                  priorities, trackers)

    # we initialize the options object that we will use to update the ticket
    options = {'rmine': rmine, 'ticket_id': ticket_id}

    # do_update is a flag that will be set to True if we actually need to
    # update the ticket
    do_update = False

    # for each of the properties created, we check if we need to update
    # and populate "options" accordingly.
    for prop in properties.itervalues():
        # if at least one of the results is True, then do_update is True
        do_update = is_different(ticket_id, options, prop) or do_update

    if do_update:
        update(**options)