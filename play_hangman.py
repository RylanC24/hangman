import requests
import game_utilities

# Define some global parameters. If this list got too much bigger it would
# probably make sense to move these to a config file.
api_url = 'http://hangman-api.herokuapp.com/hangman'
dictionary_file = './words.txt'
MAX_INCORRECT_GUESSES = 5

# Load dictionary
word_list = game_utilities.load_dictionary(dictionary_file)

# Initialize the game
response = requests.post(api_url)
token = response.json()['token']
hangman_string = response.json()['hangman']

# Before making our first guess we can update our word_list based on the
# hangman_string we received from the API and our (currently empty) list of
# previous guesses
previous_guesses = []
word_list = game_utilities.filter_word_list(
    word_list,
    hangman_string,
    previous_guesses
)

# Now we actually play the game by making a series of guesses
n_guesses = 0
while n_guesses < MAX_INCORRECT_GUESSES:
    print("Current hangman string:", hangman_string)
    guess = game_utilities.get_next_guess(word_list, previous_guesses)
    previous_guesses.append(guess)

    # Send our guess to the hangman api
    response = requests.put(api_url, data={'token': token, 'letter': guess})
    # Update the token and hangman_string
    token = response.json()['token']
    hangman_string = response.json()['hangman']

    # Check to see if the guess was correct or not
    if response.json()['correct']:
        # Check to see if we won the game!
        if '_' not in hangman_string:
            print("YOU WON THE GAME!")
            print(hangman_string)
            break
        else:
            print("Correct guess:", guess)
    else:
        n_guesses += 1
        print("Wrong guess:", guess)

    # Before making another guess we should update our word_list based on
    # the information we received from the last guess
    word_list = game_utilities.filter_word_list(
        word_list,
        hangman_string,
        previous_guesses
    )

if n_guesses == MAX_INCORRECT_GUESSES:
    print("GAME OVER. You exceeded the max number of wrong guesses. :-(")
    print(hangman_string)
