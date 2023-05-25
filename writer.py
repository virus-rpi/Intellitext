import os
from dotenv import load_dotenv
from prompt import AI
import json


class writer:
    def __init__(self, name, description, book_type, api_version):
        self.description = description
        self.name = name
        self.type = book_type
        load_dotenv()
        api = os.getenv("API-KEY")
        self.ai = AI([api_version, api])
        self.data = {
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'book': [],
            'chapter_summary': [],
            'chapter_count': 0,
        }
        if os.path.isfile(self.name + ".json"):
            self.load()
        self.save()

    def write(self, prompt):
        chapter = self.ai.prompt(prompt)
        summary = self.ai.summarize(chapter)
        return [chapter, summary]

    def writeNextChapter(self):
        chapter, summary = self.write(
            f"""The following is a {self.type} with the name {self.name} 
            It is written with great detail. 
            Description: {self.description}\n. 
            {f"Summary of last chapters: {self.data['chapter_summary'][-5:]}" if len(self.data['chapter_summary']) >= 1 else ""}
            The following is the {self.data['chapter_count'] + 1} Chapter.
            """
        )
        self.data['book'].append(chapter + "\n\n")
        self.data['chapter_summary'].append(summary)
        self.data['chapter_count'] += 1
        print(f"Chapter {self.data['chapter_count']} written")
        self.save()
        return chapter

    def save(self):
        with open(self.name + ".json", 'w') as f:
            json.dump(self.data, f)

    def load(self):
        with open(self.name + ".json", 'r') as f:
            self.data = json.load(f)
