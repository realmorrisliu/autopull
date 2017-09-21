import sys
import os
import time
from github import Github

configPath = os.path.join(os.path.expanduser('~'), '.autopullconfig')
config = {
    'username': '',
    'password': '',
    'repo': '',
    'proj': '',
}

try:
    with open(configPath, 'r') as CONFIG:
        for line in CONFIG.readlines():
            configItems = line.strip().split(':')
            config[configItems[0]] = configItems[1]

            username = config['username']
            password = config['password']
            repo = config['repo']
            proj = config['proj']

except FileNotFoundError:
    with open(configPath, 'w') as CONFIG:
        username = input('username: ')
        password = input('password: ')
        repo = input('repo: ')
        proj = input('proj: ')

        CONFIG.write('username:{0}\npassword:{1}\nrepo:{2}\nproj:{3}\n'.format(username, password, repo, proj))

g = Github(username, password)
repo = g.get_user().get_repo(repo)
os.chdir(proj)

isUpToDate = True

try:
    while True:
        with open('.git/HEAD', 'r') as HEAD:
            branchName = os.path.split(HEAD.readline().strip())[1]

        branch = repo.get_branch(branchName)

        if isUpToDate:
            sys.stdout.write("\r" + time.asctime(time.localtime(time.time())))
            sys.stdout.flush()
            with open('.git/logs/refs/heads/{0}'.format(branchName), 'r') as refsHEAD:
                for line in refsHEAD.readlines():
                    isUpToDate = line.find(branch.commit.sha) > -1
        else:
            print('\nSyncing...')
            os.system('git pull')
            isUpToDate = True

except KeyboardInterrupt:
    print('\nTerminated')