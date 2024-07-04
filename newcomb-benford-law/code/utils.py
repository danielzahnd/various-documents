# Import all relevant packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

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