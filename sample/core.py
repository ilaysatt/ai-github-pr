from . import helper
from openai import OpenAI
import tiktoken
import os


def gpt_convo(f, comment: bool, change: bool, post: bool):
    helper.configure()
    pull_content = helper.get_repo_pull_info()
    client = OpenAI(
        api_key=os.getenv('api_key')
    )
    request = ""
    if comment:
        if change:
            request = ("Generate clear, concise, and actionable PR comments that provide constructive feedback to the "
                       "developer. In addition to comments, suggest specific, practical, and easy-to implement changes "
                       "to improve the code. ")
        else:
            request = ("Generate clear, concise, and actionable PR comments that provide constructive feedback to the "
                       "developer. ")
    elif change:
        request = "Suggest specific, practical, and easy-to implement changes to improve the code. "

    sys_messages = {"role": "system", "content": "You are a tool that analyzes changes in GitHub pull requests, "
                                                 "understanding the context and impact on the overall codebase. "}
    for content in pull_content:
        for file in content[2]:
            message = "This is the patch, i.e. the changes made to the file: " + file[2] + ("\n This is the file "
                                                                                            "content before the "
                                                                                            "changes: ") + file[1]
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            if len(encoding.encode(message)) > 4097:
                continue
            chat_completion = client.chat.completions.create(
                messages=[sys_messages, {"role": "user", "content": request + message}],
                model="gpt-3.5-turbo"
            )
            print(chat_completion.choices[0].message.content)
