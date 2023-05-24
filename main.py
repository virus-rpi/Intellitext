from flask import Flask
from writer import writer

# app = Flask(__name__)


# @app.route('/')
# def index():
#     return "Hello World"


# app.run(host='localhost')

if __name__ == "__main__":
    print("Welcome")
    book1 = writer("The Dino", "A story about a clumsy T-Rex and it's adventures", "Novel")
    print(book1)
    while 1:
        book1.writeNextChapter()
