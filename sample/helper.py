from github import Github
from github import Auth
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


def get_repo_pull_info():
    configure()
    auth = Auth.Token(os.getenv('github_access_token'))
    g = Github(auth=auth)
    #repo_info = os.popen('git remote get-url origin').read().strip().split('/')[-2:]
    #repo_owner, repo_name = repo_info[0].split(':')[1], repo_info[1].replace('.git', '')
    #repo = g.get_repo(f"{repo_owner}/{repo_name}")
    repo = g.get_repo("openai/openai-python")
    repo_pulls = repo.get_pulls()
    pull_content = []
    for pull in repo_pulls:
        pull_content.append([[]] * 3)
        pull_content[-1][0] = pull.number
        pull_content[-1][1] = pull.title
        for file in pull.get_files():
            pull_content[-1][2].append([file.filename, repo.get_contents(file.filename).decoded_content.decode(), file.patch])
    return pull_content


def extract_file(f: str):
    try:
        with open(f, "r") as file:
            data = file.read()
            file.close()
    except IOError:
        print("No " + f + " file found")
        return 0
    return data


if __name__ == '__main__':
    get_repo_pull_info()
