from nomic.gpt4all import GPT4All
import openai


class AI:
    def __init__(self, args):
        self.ai_type = args[0]
        if self.ai_type == "openai":
            openai.api_key = args[1]
        elif self.ai_type == "local":
            self.m = GPT4All()
            self.m.open()

    def prompt(self, prompt):
        response = "No AI available"
        if self.ai_type == "openai":
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=1,
                max_tokens=1500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )["choices"][0]["text"]
        elif self.ai_type == "local":
            response = self.m.prompt(prompt)
        elif self.ai_type == "debug":
            print(prompt)
            response = "Debug enabled!"
        return response

    def summarize(self, chapter):
        response = "No AI available"
        if self.ai_type == "openai":
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"{chapter}\n\nThe same text summarized in one sentence:\n\n",
                temperature=1,
                max_tokens=110,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )["choices"][0]["text"]
        elif self.ai_type == "local":
            response = self.m.prompt(f"{chapter}\n\nThe same text summarized in one sentence:\n\n")
        elif self.ai_type == "debug":
            response = "Debug enabled!"
        return response

