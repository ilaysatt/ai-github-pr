from . import helper
from openai import OpenAI
import tiktoken
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="A comment generator for GitHub pull-requests, based on OpenAI.")
    parser.add_argument("-p", "--post", help="Post comments to GitHub", action="store_true", default=False)
    helper.configure()
    args = parser.parse_args()
    pull_content = helper.get_repo_pull_info()
    client = OpenAI(
        api_key=os.getenv('api_key')
    )
    request = ("Generate clear, concise, and actionable PR comments that provide constructive feedback to the "
               "developer. In addition to comments, suggest specific, practical, and easy-to implement changes "
               "to improve the code. ")

    sys_messages = {"role": "system", "content": "You are a tool that analyzes changes in GitHub pull requests, "
                                                 "understanding the context and impact on the overall codebase. "}
    for content in pull_content:
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
            chat_completion = client.chat.completions.create(
                messages=[sys_messages, {"role": "user", "content": message}],
                model="gpt-3.5-turbo"
            )
            file.append(chat_completion.choices[0].message.content)
            print(chat_completion.choices[0].message.content)
    if args.post:
        helper.upload_repo_pull_comments(pull_content)


if __name__ == "__main__":
    main()
