#! /usr/bin/python
# ~*~ coding: utf-8 ~*~

from github3 import login
from datetime import datetime
import json
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

USER = config.get('GitHub', 'USER')
PWD = config.get('GitHub', 'PWD')
ORG = config.get('GitHub', 'ORG')
FILE = config.get('GitHub', 'FILE')
COMMITS = config.getint('GitHub', 'COMMITS')
REPOS = eval(config.get('GitHub', 'REPOS'))
START = eval(config.get('Sprint', 'START'))

# pip install github3.py

def generate_report(org):
    projects = []
    repos = [repo for repo in org.iter_repos() if repo.name in REPOS]
    for repo in repos:
        commits = [x.commit for x in repo.iter_commits(since=START)]
        project = {
            "name": repo.name,
            "commits": [
                {
                    # 'author': x.author,
                    # 'committer': x.committer,
                    'sha': x.sha[:8], # displays the first 8 characters of the sha
                    # keeps only the first line of the commit message
                    'message': x.message.split("\n", 1)[0]
                } for x in commits[0:COMMITS]
            ]
        }

        projects.append(project)

    return { "projects": sorted(projects, key=lambda project: project['name']) } 

if __name__ == '__main__':
    gh = login(USER, password=PWD)
    sysfera = gh.organization(ORG)
    data = generate_report(sysfera)
    data_file = open(FILE, 'w')
    json.dump(data, data_file, indent=4)
    
