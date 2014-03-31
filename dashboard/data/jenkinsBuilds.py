#! /usr/bin/pythonpip install jenkins-webapi
# ~*~ coding: utf-8 ~*~

from jenkins import Jenkins
import json

# pip install jenkins-webapi

JENKINS_URL = "http://192.168.1.2/jenkins"
JENKINS_USER = "dashboard"
JENKINS_PWD = "dashboard"
DATA_FILE = "dataJenkins.json"
PROJECTS = ["libbatch", "vishnu-automtest", "vishnu-compil", "WB"]


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
    jenkins = Jenkins(JENKINS_URL, JENKINS_USER, JENKINS_PWD)
    data = generate_report(jenkins)
    data_file = open(DATA_FILE, 'w')
    json.dump(data, data_file, indent=4, sort_keys=True)
