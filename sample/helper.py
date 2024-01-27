from github import Github
from github import Auth
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


def get_repo_info():
    configure()
    auth = Auth.Token(os.getenv('github_access_token'))
    g = Github(auth=auth)
    repo = g.get_repo("openai/openai-python")
    for pull in repo.get_pulls():
        print("pull is", pull.title)
        #for file in pull.get_files():
        #    print("file is", file.filename)
        #    print(file.patch)
    current_directory = os.getcwd()
    repo_info = os.popen('git remote get-url origin').read().strip().split('/')[-2:]
    repo_owner, repo_name = repo_info[0].split(':')[1], repo_info[1].replace('.git', '')
    print(f"{repo_owner}/{repo_name}")
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    print(repo.name)


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
    get_repo_info()



