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
            [
                self.type,
                self.name,
                self.description,
                self.data
            ]
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
