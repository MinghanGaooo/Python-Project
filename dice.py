# dice.py
# by Prof. Bracy, AWB93, April, 2023

""" A module that supports rolling and displaying lone dice."""

# STUDENTS: do NOT modify this file. you will not submit it for A6 or A7

import random, printer

random.seed(11)

""" Helper class that simplifies the ascii art stringification of a die."""
class Dots():

    NUM_ROWS = 5    # ascii art dice are 5 rows tall

    # all ascii art dice begin and end with line.
    # the middle rows are a combination of these other 5 strings
    line = ".-------."
    nada = "|       |"
    one  = "|   O   |"
    two  = "| O   O |"
    left = "| O     |"
    right= "|     O |"

    """Below is a list of lists. Each list contains the strings needed to
    print out each of the possible dice you might want to draw.

    Example: a dice with value 4 is:
        ".-------."   line
        "| O   O |"   two
        "|       |"   nada
        "| O   O |"   two
        ".-------."   line
    so below you'll see art[4] set to [line,two,nada,two,line]
    """
    art = [[line,nada,nada,nada,line], # the empty Die
           [line,nada,one,nada,line],  # a Die with value 1
           [line,left,nada,right,line],# a Die with value 2
           [line,left,one,right,line], # a Die with value 3
           [line,two,nada,two,line],   # a Die with value 4
           [line,two,one,two,line],    # a Die with value 5
           [line,two,two,two,line]]    # a Die with value 6

class Die():
    """Instances are 6-sided dice.

    This is a somewhat simplified version of the Die introduced in lecture.
    This is all you need for A6 and A7.
    """

    NUM_SIDES = 6

    def __init__(self, val=None):
        """ Initializer: makes a new Die
            Precondition: val must be an integer from 1 to 6
                          if no val provided, value will be chosen randomly
        """
        if val != None:
            assert type(val)== int, "die value must be an int"
            assert val > 0, "die value must be greater than 0"
            assert val <= Die.NUM_SIDES, "die value can be at most " + \
                str(Die.NUM_SIDES)
            self.value = val
        else:
            self.roll()

    def __str__(self):
        """Returns: the ascii art string version of the die"""
        mystring = ""
        for row in range(Dots.NUM_ROWS):
            mystring += Dots.art[self.value][row]+"\n"
        return mystring

    def roll(self):
        """ Picks a new random integer to be the new value of the Die """
        self.value = random.randint(1,Die.NUM_SIDES) # invariant maintained

if __name__=='__main__':
    d = Die()
    printer.print_it(d) # just to show you that we already drew a Die for you
