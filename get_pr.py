from github import Github
from github import PullRequest
from github import Auth
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


configure()
auth = Auth.Token(os.getenv('github_access_token'))

g = Github(auth=auth)
repo = g.get_repo("openai/openai-python")
pull_request = repo.get_pull(1050)
files = pull_request.get_files()[0].patch
print(files)
#for repo in g.get_user().get_repos():
#    print(repo.name)
#    # to see all the available attributes and methods
#    print(dir(repo))
