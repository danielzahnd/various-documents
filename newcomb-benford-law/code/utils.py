# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import re
from word2number import w2n

# Set parameters of packages
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = r'\usepackage{bm, amsmath, siunitx}'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams['font.size'] = 18

# Define Benford's law
def benford(array):
    '''
    This function implements Benford's law, which is calculated for every entry in array.

    INPUT
    -----
    array (array): Array of floats

    OUTPUT
    ------
    array_benford (array): Array of floats, calculated with Benford's law using array as input
    '''
    return np.log10(1 + 1/array)

# Define function to identify first digit 1,...,9 of all numbers in an array
def find_first_digits(array):
    '''
    This function finds the first digit 1,...,9 of every number in the input array.

    INPUT
    -----
    array (array): Array of floats

    OUTPUT
    ------
    first_digits (array): First digits 1,...,9 of numbers in input array
    '''
    # Define array
    first_digits = np.zeros(len(array))

    # Loop over all entries in array
    for i in range(len(array)):
        # Convert number to string
        num_str = str(array[i])
        
        # Iterate through characters until the first nonzero digit is found
        for digit in num_str:
            if digit != '0' and digit != '.' and digit != ',':
                first_digits[i] = int(digit)
                break

    # Return array of first digits
    return first_digits

# Define function to extract word-based numbers from a text file
def extract_number_phrases(words):
    '''
    This function extracts sequences of number-related words (e.g. "twenty one", "three hundred")
    from a list of individual words. Each sequence is returned as a list of words.

    INPUT
    -----
    words (list of str): A list of words, typically obtained from text.split()

    OUTPUT
    ------
    word_number_phrases (list of list of str): List of number word sequences
    '''
    # Define acceptable number words
    number_vocab = [
        'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
        'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen',
        'eighteen', 'nineteen', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',
        'eighty', 'ninety', 'hundred', 'thousand', 'million', 'billion', 'trillion', 'and'
    ]

    # Define iterables
    word_number_phrases = []
    i = 0

    # Iterate through all words in the list
    while i < len(words):
        phrase = []

        # If current word is number-related, start collecting the phrase
        while i < len(words) and words[i] in number_vocab:
            phrase.append(words[i])
            i += 1

        # Clean up 'and' at start/end of phrase or move to next word if current is not a number word
        if phrase:
            if phrase[0] == 'and':
                phrase = phrase[1:]
            if phrase and phrase[-1] == 'and':
                phrase = phrase[:-1]

            # Append number if phrase is not empty
            if phrase:
                word_number_phrases.append(phrase)
        else:
            i += 1

    # Return found numbers as phrases
    return word_number_phrases

# Define a function to convert found word-based numbers to digit-based numbers
def words_to_num(words):
    '''
    This function converts a list of number-related words into its corresponding integer.

    INPUT
    -----
    words (list of str): Number-related words, e.g. ['three', 'hundred', 'twenty', 'one']

    OUTPUT
    ------
    number (int): The numeric equivalent, e.g. 321
    '''
    # Define dictionnary for word-based to digit-based number conversion
    num_dict = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
        "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
        "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
        "eighty": 80, "ninety": 90, "hundred": 100, "thousand": 1000
    }

    # Define interables
    total = 0
    current = 0

    # Iterate through all given words in a phrase describing a number
    for word in words:
        word = word.lower()

        # Ignore 'and'
        if word == 'and':
            continue

        # Check, if number word is in dictionnary
        if word in num_dict:
            val = num_dict[word]

            # Handle orders of magnitude
            if val == 100:
                current = 100 if current == 0 else current * 100
            elif val == 1000:
                total += current * 1000
                current = 0
            else:
                current += val
        else:
            pass

    # Return converted word-based number as digit-based number
    return total + current

# Define function to extract numbers from the asv bible text
def extract_numbers(filepath):
    '''
    This function finds all numbers in a bible text textfile (.txt) of the form:
    Genesis 1:10: Text, text, text.
    Genesis 1:11: More text, more text, more text.

    INPUT
    -----
    filepath (string): String filepath to the text file to read.

    OUTPUT
    ------
    numbers (array): All numbers (word-based and digit-based) found in the text
    '''
    # Read file
    f = open(filepath, "r")
    text = f.read()

    # Remove book titles, chapter, and verse numbers
    text = re.sub(r'^[A-Za-z]+\s+\d+:\d+\s+', '', text, flags=re.MULTILINE)

    # Remove punctuation, question marks and the like and make everything lowercase
    text = re.sub(r'[^\w\s]', '', text).lower()

    # Extract digit-based numbers
    digit_numbers = np.array(re.findall(r'\d+', text))  # Finds numbers like 1, 31, etc.

    # Convert text to array containg words
    words = np.array(text.split())

    # Extract number phrases
    word_numbers = extract_number_phrases(words)

    # Convert word numbers to digits
    word_numbers = np.array([words_to_num(phrase) for phrase in word_numbers])

    # Concatenate found digit-based and found word-based numbers
    numbers = np.concatenate((digit_numbers.astype(int), word_numbers))

    return numbers