#! /usr/bin/pythonpip install jenkins-webapi
# ~*~ coding: utf-8 ~*~

from jenkins import Jenkins
import json

configFile = open('config.json')
config = json.load(configFile)
configFile.close()

# pip install jenkins-webapi

URL = config['jenkins']['url']
USER = config['jenkins']['user']
PWD = config['jenkins']['pwd']
FILE = config['jenkins']['file']
PROJECTS = config['jenkins']['projects']


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
