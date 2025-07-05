#!/usr/bin/env python
import json
import time
import zipfile
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

backup_archive = Path("./backups/timestamp.zip")
with zipfile.ZipFile(backup_archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in backup_dir.rglob('*'):
        # Create a relative path for the file within the zip archive
        relative_path = file.relative_to(backup_dir.parent)
        zipf.write(file, relative_path)
