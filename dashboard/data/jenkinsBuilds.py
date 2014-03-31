#! /usr/bin/pythonpip install jenkins-webapi
# ~*~ coding: utf-8 ~*~

from jenkins import Jenkins
import json
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

# pip install jenkins-webapi

URL = config.get('Jenkins', 'URL')
USER = config.get('Jenkins', 'USER')
PWD = config.get('Jenkins', 'PWD')
FILE = config.get('Jenkins', 'FILE')
PROJECTS = eval(config.get('Jenkins', 'PROJECTS'))


statuses = { "blue": "success",
             "red": "danger",
             "notbuilt": "normal",
             "aborted": "active",
             "yellow": "warning"
         }


def generate_report(jenkins):
    """generate Jenkins report"""
    builds = []
    for job in jenkins.jobs:
        if job.name in PROJECTS:
            status = statuses[job.info['color']]
            entry = {
                "name": job.name,
                "status": status
            }
            builds.append(entry)
    return { "jenkinsBuilds": builds }


if __name__ == '__main__':
    jenkins = Jenkins(URL, USER, PWD)
    data = generate_report(jenkins)
    data_file = open(FILE, 'w')
    json.dump(data, data_file, indent=4, sort_keys=True)
