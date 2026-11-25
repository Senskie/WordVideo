from collections import Counter

def load_words(filename):
    """Load words from a text file, separated by whitespace."""

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    words = text.split()

    if not words:
        raise ValueError("The input file contains no words.")

    return words


def count_words(words):
    """Count the occurrences of each word (case-insensitive)."""

    return Counter(word.casefold() for word in words)