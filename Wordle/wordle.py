from colorama import init, Fore, Style
import random

def print_list(my_list):
    for row in my_list:
        print(row[0] + row[1] + row[2] + row[3] + row[4])

def reset_game():
    result = None
    do_reset = input("Would you like to play again? (y/n) ")

    while result is None:
        do_reset = do_reset.upper()
        if do_reset == "Y":
            result = True
        elif do_reset == "N":
            print("Shutting down...")
            result = False
        else:
            do_reset = input("Invalid response. Would you like to play again? (y/n) ")
    return result

def get_random_word(infile):
    random_word = random.choice(open(infile).read().split('\n'))
    random_word = random_word.upper()
    #print(random_word)
    return random_word

def is_valid_word(word):
    infile_name = "user_word_list.txt"
    words = open(infile_name).read().split('\n')
    if word in words:
        return True
    else:
        return False

def start_wordle():
    init()
    right_letter = Fore.GREEN + Style.NORMAL
    wrong_place = Fore.YELLOW + Style.NORMAL
    wrong_letter = Fore.BLACK + Style.BRIGHT

    running = True

    while(running):
        print("Starting a new game of Wordle!")
        solution = get_random_word("word_list.txt")
        answers = []
        guess = ""

        # Player gets 6 guesses
        for i in range(0,6):
            results = [wrong_letter] * 5
            final_results = ["\U00002B1B"] * 5
            guess = ""
            while len(guess) != 5:
                guess = input("Please enter your guess: ")
                if guess == "quit":
                    print("Shutting down...")
                    running = False
                    return
                elif len(guess) != 5:
                    print("That guess is incomplete, please try again")
                elif not is_valid_word(guess):
                    guess = ""
                    print("Guess not in word list")
                guess = guess.upper()

            index = 0
            letters_found = {}
            # right letter right place
            for letter in guess:
                if letter in solution:
                    if solution[index] == guess[index]:
                        if letter in letters_found:
                            letters_found[letter] += 1
                        else:
                            letters_found[letter] = 1
                        results[index] = right_letter
                        final_results[index] = "\N{large green square}"
                index += 1

            index = 0

            # right letter wrong place
            for letter in guess:
                if letter in solution:
                    if solution[index] != guess[index]:
                        if letter in letters_found:
                            letters_found[letter] += 1
                        else:
                            letters_found[letter] = 1
                    guess_count = guess.count(letter)
                    solution_count = solution.count(letter)
                    if solution[index] != guess[index] and letters_found[letter] <= solution_count:
                        results[index] = wrong_place
                        final_results[index] = "\N{large yellow square}"
                index += 1

            if len(results) == 5:
                print(results[0] + guess[0] + results[1] + guess[1] + results[2] + guess[2] + results[3] + guess[3] + results[4] + guess[4])
            else:
                print("Something went wrong, try again")

            answers.append(final_results)
            print(Style.RESET_ALL, end = '')
            if guess == solution:
                print(Style.RESET_ALL + "Well done! You win!")
                print_list(answers)
                if not reset_game():
                    running = False
                    return
                else:
                    break
        if guess != solution:
            print("You lost, sorry! The correct answer was " + right_letter + solution + Style.RESET_ALL)
            if not reset_game():
                running = False
                return
    return

if __name__ == '__main__':
    start_wordle()
