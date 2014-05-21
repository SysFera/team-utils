#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

import os
import argparse
import subprocess


parser = argparse.ArgumentParser(description='Front to the imdoing commands.')
parser.add_argument('command',
                    type=str,
                    help='the imdoing command to run',
                    choices=["mine", "current", "create", "assign", "start", "stop"])
parser.add_argument('arguments',
                    nargs=argparse.REMAINDER,
                    help='the command arguments')
args = parser.parse_args()

command = args.command
for index, arg in enumerate(args.arguments):
    if arg[0] != "-":
        args.arguments[index] = '\"' + arg + '\"'
arguments = " ".join(args.arguments)


def get_dir():
    directory = os.environ.get('TEAM_PATH')

    if directory is not None:
        return os.path.join(directory, "imdoing")
    else:
        print "The environment variable TEAM_PATH is not set. Aborting."
        quit()


def mine(directory):
    script = os.path.join(directory, "mine.py")
    subprocess.call("python " + script + " " + arguments, shell=True)


def current(directory):
    script = os.path.join(directory, "target.py")
    subprocess.call("python " + script + " " + arguments, shell=True)


def create(directory):
    script = os.path.join(directory, "create.py")
    subprocess.call("python " + script + " " + arguments, shell=True)


def assign(directory):
    script = os.path.join(directory, "assign.py")
    subprocess.call("python " + script + " " + arguments, shell=True)


def start(directory):
    script = os.path.join(directory, "time.py")
    subprocess.call("python " + script + " start " + arguments, shell=True)


def stop(directory):
    script = os.path.join(directory, "time.py")
    subprocess.call("python " + script + " stop " + arguments, shell=True)


def main():
    directory = get_dir()
    options = {
        "mine": mine,
        "current": current,
        "create": create,
        "assign": assign,
        "start": start,
        "stop": stop
    }

    options[command](directory)

    quit()


if __name__ == '__main__':
    main()