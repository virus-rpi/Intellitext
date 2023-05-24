from writer import writer

if __name__ == "__main__":
    print("Welcome")
    book1 = writer("The Dino", "A story about a clumsy T-Rex and it's adventures", "Novel")
    print(book1)
    while 1:
        book1.writeNextChapter()
