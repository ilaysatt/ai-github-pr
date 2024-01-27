from . import helper
from openai import OpenAI
import os


def gpt_convo(f, comment: bool, change: bool, post: bool):
    patch = ("+\t prittt(hlo wr')"
             "-\t print('hello world')")
    f = "print('hello world')"
    helper.configure()
    helper.github_api_call()
    client = OpenAI(
        api_key=os.getenv('api_key')
    )
    request = ""
    if comment:
        if change:
            request = ("Given the following changes made in the pull-request, displayed through a patch, what comments "
                       "would you make in the pull request? Additionally write the changes in code.")
        else:
            request = ("Given the following changes made in the pull-request, displayed through a patch, what comments "
                       "would you make in the pull request?")
    elif change:
        request = ("Given the following changes made in the pull-request, displayed through a patch, write changes "
                   "you would make in the code.")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": request + " This is the patch: " + patch + "\n This is the file contents: " + f
                            }
        ],
        model="gpt-3.5-turbo",
    )
    print(chat_completion.choices[0].message.content)

