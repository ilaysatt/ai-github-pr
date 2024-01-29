from . import helper
from openai import OpenAI
import tiktoken
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="A comment generator for GitHub pull-requests, based on OpenAI.")
    parser.add_argument("-u", "--upload", default=False, help="Upload comments to GitHub", action="store_true")
    parser.add_argument("-r", "--repo", type=str, default=None, help="Which repository to check. The default "
                                                                     "repository is your current directory. The "
                                                                     "format is {repo_owner}/{repo_name}")
    parser.add_argument("-e", "--env", type=str, default=None, help="Location of .env file to use. The format of the "
                                                                    ".env should as follows:\n"
                                                                    "\napi_key={github_api_key}\n"
                                                                    "github_access_token={github_access_token}")
    parser.add_argument('-pr', '--pull-requests-id', type=int, default=-1, help="ID of the pull-request. If no ID is "
                                                                                "provided, all the repo's pull "
                                                                                "requests will be checked")
    args = parser.parse_args()
    helper.configure(args.env)
    pull_content = helper.get_repo_pull_info(args.repo, args.pull_requests_id)

    client = OpenAI(
        api_key=os.getenv('api_key')
    )
    request = ("Generate clear, concise, and actionable PR comments that provide constructive feedback to the "
               "developer. In addition to comments, suggest specific, practical, and easy-to implement changes "
               "to improve the code. ")

    sys_messages = {"role": "system", "content": "You are a tool that analyzes changes in GitHub pull requests, "
                                                 "understanding the context and impact on the overall codebase. "}
    for content in pull_content:
        print(f"\nPull-request {content[0]}: {content[1]}")
        for file in content[2]:
            if not file[1]:
                message = request + "This is the file: " + file[2] + (". Ignore the pluses and minuses in the "
                                                                      "beginning of the"
                                                                      "lines.")
            else:
                message = request + "This is the patch, i.e. the changes made to the file: " + file[2] + (
                    "\n This is the file "
                    "content before the "
                    "changes: ") + file[1]
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            if len(encoding.encode(message)) > 4097:
                if file[1]:
                    message = request + "This is the patch, i.e. the changes made to the file: " + file[2]
                    if len(encoding.encode(message)) > 4097:
                        file.append(None)
                        continue
                else:
                    file.append(None)
                    continue
            print(f"\nRegarding file: {file[0]}")
            chat_completion = client.chat.completions.create(
                messages=[sys_messages, {"role": "user", "content": message}],
                model="gpt-3.5-turbo"
            )
            file.append(chat_completion.choices[0].message.content)
            print(chat_completion.choices[0].message.content)
        print("---------------")
    if args.upload:
        print("Uploading the comments to GitHub...")
        helper.upload_repo_pull_comments(pull_content, args.repo)


if __name__ == "__main__":
    main()
