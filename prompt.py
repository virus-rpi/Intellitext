from nomic.gpt4all import GPT4All
import openai
import gpt4free
from gpt4free import Provider


class AI:
    def __init__(self, args):
        self.ai_type = args[0]
        if self.ai_type == "openai":
            openai.api_key = args[1]
        elif self.ai_type == "local":
            self.m = GPT4All()
            self.m.open()

    def prompt(self, args):
        book_type = args[0]
        name = args[1]
        description = args[2]
        data = args[3]
        prompt = f"""The following is a {book_type} with the name {name} 
            It is written with great detail. 
            Description: {description}\n. 
            {f"Summary of last chapters: {data['chapter_summary'][-5:]}" if len(data['chapter_summary']) >= 1 else ""}
            The following is the {data['chapter_count'] + 1} Chapter.
        """

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
        elif self.ai_type == "gpt4free":
            prompt = f"""
            Write the {data['chapter_count'] + 1} chapter of a book named {name} it is about {description}.
            {f"Summary of last chapters: {data['chapter_summary'][-5:]}" if len(data['chapter_summary']) >= 1 else ""}
            Please write the chapter with great detail.
            """
            response = gpt4free.Completion.create(
                Provider.You, prompt=prompt,
            )
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
        elif self.ai_type == "gpt4free":
            response = gpt4free.Completion.create(
                Provider.You, prompt=f"Summarize the following text in one Sentence:\n{chapter}\n\n"
            )
        return response
