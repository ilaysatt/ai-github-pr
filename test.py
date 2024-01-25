from openai import OpenAI
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


configure()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("api_key")
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Given the following changes made in the pull-request, what comments would you make?"
                       "This is the code before:"
                        "print('hello world')"
                        "this is the code after:"
                        "pnt('hello worl"
                        }
    ],
    model="gpt-3.5-turbo",
)
print(chat_completion.choices[0].message.content)
