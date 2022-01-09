def get_valid_words(length=5):
    corpus = open("Wordle/words_alpha.txt")
    words = [word for word in corpus.read().split() if len(word) == length]


    textfile = open("Wordle/user_word_list.txt", "w")
    for word in words:
        textfile.write(word.upper() + "\n")
    textfile.close()

def get_solution_words(length=5):
    corpus = open("Wordle/wordlist.mit.txt")
    words = [word for word in corpus.read().split() if len(word) == length]


    textfile = open("Wordle/word_list.txt", "w")
    for word in words:
        textfile.write(word.upper() + "\n")
    textfile.close()
