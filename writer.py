import os
from dotenv import load_dotenv
from prompt import AI
import json


class writer:
    def __init__(self, name, description, book_type):
        self.description = description
        self.name = name
        self.type = book_type
        load_dotenv()
        api = os.getenv("API-KEY")
        self.ai = AI(["openai", api])
        self.data = {
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'book': "",
            'chapter_summary': [],
            'chapter_count': 1,
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
            Summary of last 3 chapters: {self.data['chapter_summary'][-3:]} 
            Chapter {self.data['chapter_count']}\n"""
        )
        self.data['book'] = self.data['book'] + chapter + "\n\n"
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


if __name__ == "__main__":
    book1 = writer("The Dino", "A story about a clumsy T-Rex and it's adventures", "Novel")
    while 1:
        book1.writeNextChapter()
