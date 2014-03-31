#! /usr/bin/python
# ~*~ coding: utf-8 ~*~

from github3 import login
from datetime import datetime
import json

USER = "sysfera-jenkins2"
PWD = "GraalSystems123"
ORG = "SysFera"
DATA_FILE = "github.json"
BLESSED_REPOS = ["libbatch", "webboard", "vishnu"]
DATE_START = datetime(2014, 3, 25)

# pip install github3.py

def generate_report(org):
    clog = {}
    repos = [repo for repo in org.iter_repos() if repo.name in BLESSED_REPOS]
    for repo in repos:
        commits = [x.commit for x in 
                   repo.iter_commits(since=DATE_START)]
        clog[repo.name] = [{ 'author': x.author,
                             'committer': x.committer,
                             'sha': x.sha,
                             'message': x.message } for x in commits]

    return clog


if __name__ == '__main__':
    gh = login(USER, password=PWD)
    sysfera = gh.organization(ORG)
    data = generate_report(sysfera)
    data_file = open(DATA_FILE, 'w')
    json.dump(data, data_file, indent=4)
    
