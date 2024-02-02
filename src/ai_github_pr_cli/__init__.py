from . import helper
from openai import OpenAI
import tiktoken
import os
import argparse


def main():
    """
    Fetches code from pull-requests and generates comments / code changes using OpenAI API
    :returns: None
    """
    parser = argparse.ArgumentParser(description="A comment generator for GitHub pull-requests, based on OpenAI.")
    parser.add_argument("-u", "--upload", default=False, help="Upload comments to GitHub", action="store_true")
    parser.add_argument("-r", "--repo", type=str, default=None, help="Which repository to check. The default "
                                                                     "repository is the one that is associated with "
                                                                     "your current directory. The format is {"
                                                                     "repo_owner}/{repo_name}")
    parser.add_argument("-e", "--env", type=str, default=None, help="Path of .env file to use. The format "
                                                                    "of the .env should as follows:\n"
                                                                    "\nOPENAI_API_KEY={your_openai_api_key}\n"
                                                                    "GITHUB_TOKEN={your_github_token}")
    parser.add_argument('-pr', '--pull-requests-id', type=int, default=-1, help="ID of the pull-request. If no ID is "
                                                                                "provided, all the repo's pull "
                                                                                "requests will be checked")
    parser.add_argument('-q', '--quite', default=False, action="store_true", help="Don't print generated comments and "
                                                                                  "suggestions to cli")
    args = parser.parse_args()
    if args.env:
        helper.configure(args.env)
    print("Fetching pull-request(s) + file(s)...")
    pull_content = helper.get_repo_pull_info(args.repo, args.pull_requests_id)

    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )
    request_comment = ("Generate clear, concise, and actionable PR comments that provide constructive feedback to the "
                       "developer. ")
    request_suggestion = "Suggest specific, practical, and easy-to implement changes to improve the code. "

    sys_messages = {"role": "system", "content": "You are a tool that analyzes changes in GitHub pull requests, "
                                                 "understanding the context and impact on the overall codebase. "}
    for content in pull_content:
        print(f"\nPull-request {content['pull number']}: {content['pull title']}")

        for file in content['files']:
            print(f"\nRegarding file: {file['filename']}...")
            if not file['file content']:
                message_comment = request_comment + "This is the file: " + file['file patch'] + (". Ignore the pluses "
                                                                                                 "and minuses in the "
                                                                                                 "beginning of the "
                                                                                                 "lines.")
                message_suggestion = request_suggestion + "This is the file: " + file['file patch'] + (
                    ". Ignore the pluses and "
                    "minuses in the"
                    "beginning of the"
                    "lines.")
            else:
                message_comment = (request_comment + "This is the patch, i.e. the changes made to the file: " +
                                   file['file patch'] + (
                                       "\n This is the file "
                                       "content before the "
                                       "changes: ") + file['file content'])
                message_suggestion = request_suggestion + "This is the patch, i.e. the changes made to the file: " + \
                                     file['file patch'] + (
                                         "\n This is the file "
                                         "content before the "
                                         "changes: ") + file['file content']
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            if len(encoding.encode(message_comment)) > 4097 or len(encoding.encode(message_suggestion)) > 4097:
                if file['file content']:
                    message_comment = (request_comment + "This is the patch, i.e. the changes made to the file: " +
                                       file['file patch'])
                    message_suggestion = (
                            request_suggestion + "This is the patch, i.e. the changes made to the file: " +
                            file['file patch'])
                    if len(encoding.encode(message_comment)) > 4097 or len(encoding.encode(message_suggestion)) > 4097:
                        file['comment'] = None
                        print("File token too large for OpenAI API. Continuing...")
                        continue
                else:
                    file['comment'] = None
                    print("File token too large for OpenAI API. Continuing...")
                    continue
            print("Processing comment...")
            chat_completion = client.chat.completions.create(
                messages=[sys_messages, {"role": "user", "content": message_comment}],
                model="gpt-3.5-turbo"
            )
            file['comment'] = chat_completion.choices[0].message.content
            if not args.quite:
                print(file['comment'])
            print("\nProcessing code suggestion...")
            chat_completion = client.chat.completions.create(
                messages=[sys_messages, {"role": "user", "content": message_suggestion}],
                model="gpt-3.5-turbo"
            )
            file['code suggestion'] = chat_completion.choices[0].message.content
            if not args.quite:
                print(file['code suggestion'])
            print("--------")
        print("*****************")
    if args.upload:
        print("Uploading the comments to GitHub...")
        helper.upload_repo_pull_comments(pull_content, args.repo)
