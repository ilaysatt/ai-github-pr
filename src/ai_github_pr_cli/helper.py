from github import Github
from github import Auth
from github import GithubException
from dotenv import load_dotenv
import os


def configure(env_location=None):
    """
    Loads environment variables
    :param env_location: env file as string
    :return: None
    """
    load_dotenv(dotenv_path=env_location)


def get_repo_pull_info(repo_full_name=None, pr_id=-1):
    """
    Returns pull-request information,
    :param repo_full_name: Full name of the repository, in the format of <repo_name>/<repo_full_name>
    :param pr_id: Pull request id
    :return: A list of pull-request information, including name, ID and files
    """
    auth = Auth.Token(os.getenv('GITHUB_TOKEN'))
    g = Github(auth=auth)
    # If repo name isn't provided, look for repo controlling current directory
    if not repo_full_name:
        repo_info = os.popen('git remote get-url origin').read().strip().split('/')[-2:]
        repo_owner, repo_name = repo_info[0].split(':')[1], repo_info[1].replace('.git', '')
        repo_full_name = f"{repo_owner}/{repo_name}"
    repo = g.get_repo(repo_full_name)
    # If pull-request ID isn't provided, extract all the repository's pull-requests
    if pr_id == -1:
        repo_pulls = repo.get_pulls()
    else:
        repo_pulls = [repo.get_pull(pr_id)]
    pull_content = []
    for pull in repo_pulls:
        pull_filenames = []
        for file in pull.get_files():
            pull_filenames.append(file.filename)
        commits = pull.get_commits()
        pull_content.append({'pull number': pull.number, 'pull title': pull.title, 'files': []})
        for commit in commits:
            for file in commit.files:
                if file.filename not in pull_filenames:
                    continue
                try:
                    file_content = repo.get_contents(file.filename).decoded_content.decode()
                except GithubException:
                    file_content = None
                    pass
                pull_content[-1]['files'].append({'filename': file.filename, 'file content': file_content,
                                                  'file patch': file.patch, 'commit': commit})

    return pull_content


def upload_repo_pull_comments(pull_content, repo_full_name=None):
    """
    Uploads generated comments and code changes to GitHub repository pull-requests
    :param pull_content: A list of pull-request information, including name, number and files
    :param repo_full_name: Full name of the repository, in the format of <repo_name>/<repo_full_name>
    :return:
    """
    auth = Auth.Token(os.getenv('GITHUB_TOKEN'))
    g = Github(auth=auth)
    # If repo name isn't provided, look for repo controlling current directory
    if not repo_full_name:
        repo_info = os.popen('git remote get-url origin').read().strip().split('/')[-2:]
        repo_owner, repo_name = repo_info[0].split(':')[1], repo_info[1].replace('.git', '')
        repo_full_name = f"{repo_owner}/{repo_name}"
    repo = g.get_repo(repo_full_name)
    for content in pull_content:
        pull_request = repo.get_pull(content['pull number'])
        for file in content['files']:
            if file['comment']:
                pull_request.create_review_comment(file['comment'], commit=file['commit'], path=file['filename'],
                                                   subject_type='file')
                pull_request.create_review(
                    body=file['code suggestion'],
                    commit=file['commit'],
                    event="REQUEST_CHANGES",
                )
