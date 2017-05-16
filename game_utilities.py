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
