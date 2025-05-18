import json
import time
import math
import requests
import subprocess
from pathlib import Path

def create_bkp_dir():
    backup_dir = Path('github.com'+'/'+str(math.floor(time.time())))
    backup_dir.mkdir(parents = True)
    return(backup_dir)

def get_repo_list():
    url = f"https://api.github.com/users/iranvir/repos"
    response = requests.get(url)
    repos_url = []
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            repos_url.append(f"https://github.com/{repo['full_name']}")
        return repos_url
    else:
        print(f"Error: Unable to fetch repositories (Status code: {response.status_code})")
        return []

def main():
    backup_dir = create_bkp_dir()
    repo_list = get_repo_list()
    
    print(backup_dir)


if __name__ == '__main__':
    main()
