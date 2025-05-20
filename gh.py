import json
import time
import math
import requests
import subprocess
from pathlib import Path


def main():

    backup_dir = Path('github.com'+'/'+str(math.floor(time.time())))
    backup_dir.mkdir(parents = True)

    user_url = f"https://api.github.com/users/iranvir/repos"
    response = requests.get(user_url)
    repos = response.json()

    for repo in repos:
        print(repo['ssh_url'])

if __name__ == '__main__':
    main()
