import github.PullRequest
from github import Github
from github import Auth
from github import GithubException
from dotenv import load_dotenv
import os


def configure(env_location=None):
    if not env_location:
        current_directory = os.getcwd()
        env_path = os.path.join(current_directory, '.env')
    else:
        env_path = env_location
    load_dotenv(dotenv_path=env_path)


def get_repo_pull_info(repo_full_name=None, pr_id=-1):
    auth = Auth.Token(os.getenv('github_access_token'))
    g = Github(auth=auth)
    if not repo_full_name:
        repo_info = os.popen('git remote get-url origin').read().strip().split('/')[-2:]
        repo_owner, repo_name = repo_info[0].split(':')[1], repo_info[1].replace('.git', '')
        repo_full_name = f"{repo_owner}/{repo_name}"
    repo = g.get_repo(repo_full_name)
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
        pull_content.append([[]] * 3)
        pull_content[-1][0] = pull.number
        pull_content[-1][1] = pull.title
        for commit in commits:
            for file in commit.files:
                if file.filename not in pull_filenames:
                    continue
                try:
                    file_content = repo.get_contents(file.filename).decoded_content.decode()
                except GithubException:
                    file_content = None
                    pass
                pull_content[-1][2].append(
                    [file.filename, file_content, file.patch, commit])

    return pull_content


def upload_repo_pull_comments(pull_content, repo_full_name=None):
    auth = Auth.Token(os.getenv('github_access_token'))
    g = Github(auth=auth)
    if not repo_full_name:
        repo_info = os.popen('git remote get-url origin').read().strip().split('/')[-2:]
        repo_owner, repo_name = repo_info[0].split(':')[1], repo_info[1].replace('.git', '')
        repo_full_name = f"{repo_owner}/{repo_name}"
    repo = g.get_repo(repo_full_name)
    for content in pull_content:
        pull_request = repo.get_pull(content[0])
        for file in content[2]:
            if file[-1]:
                pull_request.create_review_comment(file[-2], commit=file[3], path=file[0], subject_type='file')
                pull_request.create_review(
                    body=file[-1],
                    commit=file[3],
                    event="REQUEST_CHANGES",
                )


if __name__ == '__main__':
    get_repo_pull_info()
