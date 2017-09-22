import sys
import os
import time

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

os.chdir(proj)

try:
    isUpToDate = True
    while True:
        with open('.git/HEAD', 'r') as HEAD:
            branchName = os.path.split(HEAD.readline().strip())[1]

        command = 'curl -s -i -u {0}:{1} https://api.github.com/repos/{0}/{2}/branches/{3}'.format(username,
                                                                                                   password,
                                                                                                   repo,
                                                                                                   branchName)
        with os.popen(command) as response:
            for line in response.readlines():
                if line.find('sha') > -1:
                    commit = line.split('"')[3]
                    break
        if isUpToDate:
            sys.stdout.write("\r" + time.asctime(time.localtime(time.time())))
            sys.stdout.flush()
            with open('.git/logs/refs/heads/{0}'.format(branchName), 'r') as refsHEAD:
                for line in refsHEAD.readlines():
                    isUpToDate = line.find(commit) > -1
        else:
            print('\nSyncing...')
            os.system('git pull')
            isUpToDate = True
            os.system('clear')

except KeyboardInterrupt:
    print('\nTerminated')
