#!/usr/bin/env python

# To use this script, generate a GitHub PAT with just metadata access. If you have
# your GitHub SSH key on the device where this script is running. You will be able
# to clone all your repositories.

import json
import time
import requests
import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description="Backup Github repositories")
parser.add_argument("config", metavar="CONFIG", help="A configuration file")
args = parser.parse_args()

with open(args.config, 'r') as f:
    config = json.loads(f.read())

timestamp = str(int(time.time()))
backup_dir = Path("backups/"+timestamp)
backup_dir.mkdir(parents=True)

headers = {'Authorization': f"Bearer {config['token']}"}
url = "https://api.github.com/user/repos"

response = requests.get(url,headers=headers)
response = response.json()
repos = []
for repo in response:
    repos.append({'name' : repo['name'] , 'ssh_url' : repo['ssh_url']})

for repo in repos:
    repo_path = backup_dir / repo['name']
    repo_path.mkdir()
    subprocess.call(['git','init','--bare','--quiet'], cwd=repo_path)
    subprocess.call([
        'git',
        'fetch',
        '--force',
        '--prune',
        '--tags',
        repo['ssh_url'],
        "refs/heads/*:refs/heads/*",
        ],
        cwd=repo_path,
    )

