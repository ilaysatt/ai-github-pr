from github import Github
from github import Auth
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


def github_api_call():
    configure()
    auth = Auth.Token(os.getenv('github_access_token'))
    g = Github(auth=auth)
    repo = g.get_repo("openai/openai-python")
    for pull in repo.get_pulls():
        print("pull is", pull.title)
        for file in pull.get_files():
            print("file is", file.filename)
            print(file.patch)

if __name__ == '__main__':
    github_api_call()



