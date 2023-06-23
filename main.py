from writer import writer

if __name__ == "__main__":
    print("Welcome")
    book1 = writer("The Quantum Paradox", " In a future where time travel is possible but strictly regulated, a renowned physicist named Dr. Sebastian Kane invents a groundbreaking device that allows him to change pivotal moments in history. However, with each alteration, he begins to experience a disorienting phenomenon known as the \"Quantum Paradox,\" forcing him to confront the repercussions of tampering with the space-time continuum and question the true nature of free will and destiny.", "Novel", "gpt4free")
    for i in range(10):
        book1.writeNextChapter()
