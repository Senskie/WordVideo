from collections import Counter

def load_words(filename):
    """Load words from a text file, separated by whitespace."""

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    words = text.split()

    if not words:
        raise ValueError("The input file contains no words.")

    return words


def process_words(words):
    """
    Count word occurrences and return unique words.

    Word counting is case-insensitive.
    Original spelling and first occurrence order are preserved.
    """

    counts = Counter(word.casefold() for word in words)

    unique_words = list(dict.fromkeys(
        word.casefold() for word in words
    ))

    # Preserve the original spelling of the first occurrence
    display_words = {}
    for word in words:
        display_words.setdefault(word.casefold(), word)

    unique_words = [
        display_words[word] for word in unique_words
    ]

    return unique_words, counts