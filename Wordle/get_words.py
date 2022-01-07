corpus = open("Wordle/words_alpha.txt")
words = [word for word in corpus.read().split() if len(word) == 5]


textfile = open("Wordle/user_word_list.txt", "w")
counter = 0
for word in words:
    if (counter < 20):
        print(word)
        counter += 1;
    textfile.write(word.upper() + "\n")
textfile.close()
