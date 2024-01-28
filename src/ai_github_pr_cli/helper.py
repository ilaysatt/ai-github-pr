from github import Github
from github import Auth
from github import GithubException
from dotenv import load_dotenv
import os


def configure():
    current_directory = os.getcwd()
    env_path = os.path.join(current_directory, '.env')
    load_dotenv(dotenv_path=env_path)


def get_repo_pull_info():
    configure()
    auth = Auth.Token(os.getenv('github_access_token'))
    g = Github(auth=auth)
    repo_info = os.popen('git remote get-url origin').read().strip().split('/')[-2:]
    repo_owner, repo_name = repo_info[0].split(':')[1], repo_info[1].replace('.git', '')
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    repo_pulls = repo.get_pulls()
    pull_content = []
    for pull in repo_pulls:
        pull_content.append([[]] * 3)
        pull_content[-1][0] = pull.number
        pull_content[-1][1] = pull.title
        for file in pull.get_files():
            try:
                file_content = repo.get_contents(file.filename).decoded_content.decode()
            except GithubException:
                file_content = None
                pass
            pull_content[-1][2].append(
                [file.filename, file_content, file.patch])
    return pull_content


def upload_repo_pull_comments(pull_content):
    configure()
    auth = Auth.Token(os.getenv('github_access_token'))
    g = Github(auth=auth)
    repo_info = os.popen('git remote get-url origin').read().strip().split('/')[-2:]
    repo_owner, repo_name = repo_info[0].split(':')[1], repo_info[1].replace('.git', '')
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    for content in pull_content:
        pull_request = repo.get_pull(content[0])
        for file in content[2]:
            if file[-1]:
                pull_request.create_issue_comment("Regarding file: " + file[0] + "\n" + file[-1])


if __name__ == '__main__':
    get_repo_pull_info()
