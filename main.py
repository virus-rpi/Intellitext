from writer import writer

if __name__ == "__main__":
    print("Welcome")
    book1 = writer("Shinobi Neko No Michi", "A story about a cat named Ikki that wants to be a Shinobi (a Ninja) and it's adventures to become a Shinobi", "Novel", "local")
    while 1:
        book1.writeNextChapter()
