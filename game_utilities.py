import strings


def load_dictionary(file):
    """Load in the words from a dictionary file. Then convert all the words to
    lowercase and remove duplicates.
    """

    words = []
    with open(file, 'r') as f:
        for line in f:
            words.append(line.strip('\n'))
    file.close()
    words = list(set([word.lower() for word in words]))
    return words


def filter_word_list(word_list, hangman_string, previous_guesses):
    """Filter the word list based on the information contained in the hangman
    string and the list of previous guesses
    """

    # First filter out all of the words that have the wrong length
    word_list = [word for word in word_list if len(word) == len(hangman_string)]

    # Now we can filter out all of the words that contain the letters that we
    # incorrectly guessed.
    wrong_letters = [letter for letter in previous_guesses if letter not in hangman_string]
    for letter in wrong_letters:
        word_list = [word for word in word_list if letter not in word]

    # Finally, we can use our correct guesses to filter out all of the words
    # that do not match the form of our current hangman_string
    for i in range(len(hangman_string)):
        if hangman_string[i] is not '_':
            word_list = [word for word in word_list if word[i] == hangman_string[i]]

    return word_list
