from context import sample
import os

#sample.gpt_convo("f", True, True, False)
try:
    with open('context.py', 'r') as file:
        data = file.read()
        print(os.path.dirname('context.py'))
        file.close()
except IOError:
    print("No context.py file found")

print(data)