from colorama import init, Fore, Back, Style
import random


# formatting macros for command line output
right_letter = Fore.BLACK + Back.GREEN + Style.NORMAL
wrong_place = Fore.BLACK + Back.YELLOW + Style.NORMAL
wrong_letter = Fore.WHITE + Back.BLACK + Style.BRIGHT

# emoji macros
green_square = "\U0001F7E9"
yellow_square = "\U0001F7E8"
black_square = "\U00002B1B"

# Prints each row of the scoreboard with proper formatting
def print_list(my_list):
    for row in my_list:
        print(row[0] + row[1] + row[2] + row[3] + row[4])

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

# Starts and runs the Wordle game
def start_wordle():
    init()

    running = True
    while(running):
        print("Starting a new game of Wordle!")
        solution = get_random_word("Wordle/word_list.txt")
        answers = []
        guess = ""

        # Player gets 6 guesses
        for i in range(0,6):
            # Stores the player's results for this guess
            results = [wrong_letter] * 5
            # Stores the player's results as emojis for the final scoreboard
            final_results = [black_square] * 5
            guess = ""

            # Retrieve a valid guess from the player
            while len(guess) != 5:
                print("Please enter your guess: ", end = "")
                guess = input()
                guess = guess.upper()
                # Allow the player to quit at any time
                if guess == "QUIT":
                    print("Shutting down...")
                    running = False
                    return
                # Ensure the guess is the right length
                elif len(guess) != 5:
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
            if len(results) == 5:
                print(results[0] + guess[0] + results[1] + guess[1] +
                    results[2] + guess[2] + results[3] + guess[3] +
                    results[4] + guess[4] + Style.RESET_ALL)
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

if __name__ == '__main__':
    start_wordle()
