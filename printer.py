# printer.py
# by Prof. Bracy, AWB93, April, 2023

""" A module that does all the printing for you so you don't need to worry
about spelling or white space or punctuation. These should be the only
print statements in your entire code. Remember to remove all print statements
from A6 before you submit it.
"""

# STUDENTS: do NOT modify this file. you will not submit it for A6 or A7

print_f = True

def print_bad_mask_len(n):
    """ Precondition: n is an int """
    if print_f:
        print("Mask should be "+str(n)+" characters long.")

def print_bad_mask_01():
    if print_f:
        print("Mask can contain only 0 or 1.")

def print_rerolling(n):
    """ Precondition: n is an int """
    if print_f:
        print("re-rolling die "+str(n))

def print_it(thing):
    """ Precondition: thing is anything that can be printed """
    if print_f:
        print(thing)

def prompt_roll(n):
    """ Precondition: n is an int indicating how big a Hand is. """
    if print_f:
        print("Which dice would you like to re-roll?")
        print("For each die, 0 means keep, 1 means re-roll.")
        print("Press Return for '"+"0"*n+"'.")

def print_score(n):
    """ Precondition: n is an int """
    if print_f:
        print("Your current score is "+str(n))

def print_tally(i, b):
    """ Precondition: i is an int representing a Die value
                      b is a bool indicating whether that value is in the hand
    """
    if print_f:
        print("Got "+str(i)+"s? "+str(b))

def print_thanks():
    if print_f:
        print("Thanks for playing!")
