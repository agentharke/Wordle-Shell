from colorama import init, Fore, Back, Style
import random
import sys
import getopt
from get_words import get_valid_words, get_solution_words

# formatting macros for command line output
right_letter = Fore.BLACK + Back.GREEN + Style.NORMAL
wrong_place = Fore.BLACK + Back.YELLOW + Style.NORMAL
wrong_letter = Fore.WHITE + Back.BLACK + Style.BRIGHT

# emoji macros
green_square = "\U0001F7E9"
yellow_square = "\U0001F7E8"
black_square = "\U00002B1B"

# Number of letters per word
num_letters = 5

# Number of guesses per game
num_guesses = 6

# Welcome message to the player
def welcome(letters, guesses):
    welcome_message = ("""
Welcome to Wordle! I've chosen a secret """ + str(letters) + """-letter word. Your job is to guess the word in """ + str(guesses) + """ guesses or less.

If your guess contains a correct letter in the correct position it will be highlighted in """ + right_letter +
"""green""" + Style.RESET_ALL +

""".

If your guess contains a correct letter in the wrong position it will be highlighted in """ + wrong_place + """yellow""" + Style.RESET_ALL +
""".

Any letters that are incorrect will be highlighted in """ +
wrong_letter + """black""" + Style.RESET_ALL +

""".

Good luck!
""")

    print(welcome_message)

# prints correct usage of program
def usage():
    print("usage: wordle.py -g <guesses> -l <length> -s <solution>")

# Prints each row of the scoreboard with proper formatting
def print_list(my_list):
    print(num_letters)
    for row in my_list:
        for index in range(num_letters):
            print(row[index],end="")
        print()

# Prompts the user to reset the game, returns True if yes and False otherwise
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

# Returns a random word from the provided word list
def get_random_word(infile):
    random_word = random.choice(open(infile).read().split('\n'))
    random_word = random_word.upper()
    return random_word

# Returns True if the provided word is in the valid word list and False otherwise
def is_valid_word(word):
    infile_name = "Wordle/user_word_list.txt"
    words = open(infile_name).read().split('\n')
    if word in words:
        return True
    else:
        return False

def run_wordle(num_guesses=6, num_letters=5, forced_solution=""):
    running = True
    solution = ""
    while(running):
        if forced_solution:
            solution = forced_solution.upper()
        else:
            solution = get_random_word("Wordle/word_list.txt")
        answers = []
        guess = ""

        # Player gets 6 guesses
        for i in range(num_guesses):
            # Stores the player's results for this guess
            results = [wrong_letter] * num_letters
            # Stores the player's results as emojis for the final scoreboard
            final_results = [black_square] * num_letters
            guess = ""

            # Retrieve a valid guess from the player
            while len(guess) != num_letters:
                print("Please enter your guess: ", end = "")
                guess = input()
                guess = guess.upper()
                # Allow the player to quit at any time
                if guess == "-QUIT":
                    print("Shutting down...")
                    running = False
                    return
                # Ensure the guess is the right length
                elif len(guess) != num_letters:
                    print("That guess is the wrong length, please try again")
                # Make sure the guess is a word
                elif not is_valid_word(guess):
                    guess = ""
                    print("Guess not in word list")

            letters_found = {}

            # check for right letter right place
            for index, letter in enumerate(guess):
                if letter in solution:
                    if solution[index] == guess[index]:
                        # Store how many letters we've successfully guessed
                        # to avoid incorrect highlighting later
                        if letter in letters_found:
                            letters_found[letter] += 1
                        else:
                            letters_found[letter] = 1
                        results[index] = right_letter
                        final_results[index] = green_square
                index += 1

            # check for right letter wrong place
            for index, letter in enumerate(guess):
                if letter in solution:
                    if solution[index] != guess[index]:
                        # Store how many yellow letters we've guessed to
                        # avoid incorrect highlighting later
                        if letter in letters_found:
                            letters_found[letter] += 1
                        else:
                            letters_found[letter] = 1
                    guess_count = guess.count(letter)
                    solution_count = solution.count(letter)
                    # Mark letters as yellow, but only if the number of yellow
                    # letters matches the number of letters in the solution
                    if solution[index] != guess[index] and letters_found[letter] <= solution_count:
                        results[index] = wrong_place
                        final_results[index] = yellow_square
                index += 1

            # Echo the guess with proper colors
            if len(results) == num_letters:
                for index in range(num_letters):
                    print(results[index] + guess[index], end="")
                print(Style.RESET_ALL)
            else:
                print("Something went wrong, try again")

            # Add the answer to the final scoreboard
            answers.append(final_results)
            print(Back.RESET + Style.RESET_ALL, end = '')

            # Win condition
            if guess == solution:
                print(Style.RESET_ALL + "Well done! You win!")
                print_list(answers)
                if not reset_game():
                    running = False
                    return
                else:
                    break
        # Lose condition
        if guess != solution:
            print("You lost, sorry! The correct answer was " + right_letter + solution + Style.RESET_ALL)
            print_list(answers)
            if not reset_game():
                running = False
                return
    return

# Starts and runs the Wordle game
def start_wordle():
    init()

    global num_guesses
    global num_letters
    solution = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hg:l:s:",["help","guesses=",
                                "length=", "solution="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ('-g', '--guesses'):
            if not arg.isnumeric() or int(arg) < 1:
                print("error: number of guesses must be a positive integer")
                sys.exit()
            num_guesses = int(arg)
        elif opt in ('-l', '--length'):
            if not arg.isnumeric() or int(arg) < 1:
                print("error: length of guesses must be a positive integer")
                sys.exit()
            num_letters = int(arg)
        elif opt in ('-s', '--solution'):
            if not arg.isalpha():
                print("error: custom forced solutions must be strings of letters")
                sys.exit()
            solution = arg

    get_valid_words(num_letters)
    get_solution_words(num_letters)

    welcome(num_letters, num_guesses)
    run_wordle(num_guesses,num_letters,solution)

    sys.exit()

if __name__ == '__main__':
    start_wordle()
