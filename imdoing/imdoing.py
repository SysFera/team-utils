#!/usr/bin/python
# ~*~ coding: utf-8 ~*~
import argparse
import current
import mine
import create
import update
import timelog
import export
import timesheet
import raw_time_entries


def main_parser():
    parser = argparse.ArgumentParser(description='imdoing')
    subparsers = parser.add_subparsers(dest='command')
    current.add_parser(subparsers)
    mine.add_parser(subparsers)
    create.add_parser(subparsers)
    update.add_parser(subparsers)
    timelog.add_parser(subparsers)
    export.add_parser(subparsers)
    timesheet.add_parser(subparsers)
    raw_time_entries.add_parser(subparsers)
    return parser


def main():
    parser = main_parser()
    args = parser.parse_args()
    command = args.command

    if command == 'list' or command == 'current':
        current.run(args)
    elif command == 'mine':
        mine.run(args)
    elif command == 'create' or command == 'new':
        create.run(args)
    elif command == 'update' or command == 'edit':
        update.run(args)
    elif command == 'time':
        timelog.run(args)
    elif command == 'export':
        export.run(args)
    elif command == 'timesheet' or command == 'fdt':
        timesheet.run(args)


if __name__ == '__main__':
    main()