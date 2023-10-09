# a6.py
# SOLUTIONS
# PUT YOUR NETID(S) HERE
# Sources/people consulted: FILL IN OR WRITE "NONE"
# PUT DATE YOU COMPLETED THIS HERE
# Skeleton by Prof. Bracy, AWB93, April, 2023

import printer
import dice

# STUDENTS: Complete these 8 methods.
# Make sure this file has NO PRINT STATEMENTS.
# Print anything you need to print by using the printer.py helper functions


class Hand():
    """ An instance is a list of dice. The dice can be rolled, re-rolled, and
    printed in a cool ASCII art format. The hand can also add up all the values
    of its dice and state whether or not the hand has a particular number
    in it or not. (e.g., "Does this hand have any 3s?")
    """

    """ The standard terminal is 80 characters wide. Each ASCII art Die
    requires 9 characters, so we limit the number of dice in a hand to 8.

    A hand must have at least MIN_DICE dice and at most MAX_DICE dice.
    If the user asks for too many dice, they get MAX_DICE instead.
    If the user asks for too few dice, the get MIN_DICE instead.
    """
    MIN_DICE = 1
    MAX_DICE = 8

    def __init__(self, n_dice=1, dice_list=None):
        """
        Initializes the hand in one of two possible ways:
        * using the dice_list provided
        * constructing a list of dice that is n_dice long

        STUDENTS: you decide what instance attributes you'll need
                  and what to call them.

        Prints the hand after it's been initialized.

        Precondition: n_dice == len(dice_list) (if dice_list is not None)
                      MIN_DICE <= len(dice_list) <= MAX_DICE (if not None)
        """
        if dice_list != None:
            assert len(dice_list) >= Hand.MIN_DICE, \
                "dice_list must have at least "+str(Hand.MIN_DICE)+" dice"
            assert len(dice_list) <= Hand.MAX_DICE, \
                "dice_list must have at most "+str(Hand.MAX_DICE)+" dice"
            assert n_dice == len(dice_list), \
                "if dice_list is not None, its length must be n_dice"

        self.n_dice = min(max(n_dice, Hand.MIN_DICE), Hand.MAX_DICE)
        if dice_list is None:
            self.mydice = []
            for i in range(0, self.n_dice):
                self.mydice.append(dice.Die())
        else:
            self.mydice = dice_list
        # we print the hand once it's created
        printer.print_it(self)

    def get_n_dice(self):
        """ At various times, a user will need to know how many dice are in
        the Hand. So the user can call this method and be told.

        Returns: an int that represents how many dice are in the hand.
        """
        # STUDENTS: implement this method so it doesn't always return 1
        return self.n_dice

    def get_dice(self):
        """ At various times, a user will need access to the dice list
        So the user can call this method and be given a list of dice.

        Returns: a list of Die that represents the hand.
        """
        # STUDENTS: implement this method so it doesn't always return []
        return self.mydice

    def mask_valid(self, mask):
        """ A valid mask must be either:
        * the empty string
        OR
        * a string of length equal to the number of dice in the hand.
          the string must contain only 0's and/or 1's

        If the mask is the wrong length, use the helper function
        print_bad_mask_len() to inform the user.

        If the mask contains anything besides a 0 or a 1, use the helper
        function print_bad_mask_01() to inform the user.

        Returns True if the mask is valid by this definition. Otherwise False.
        """

        if (mask == ""):
            return True
        if len(mask) != self.get_n_dice():
            printer.print_bad_mask_len(self.get_n_dice())
            return False
        for c in mask:
            if c != '0' and c != '1':
                printer.print_bad_mask_01()
                return False

        return True

    def contains(self, value):
        """ Checks every die in the hand, looking for `value`

            Returns True if any die in the hand has the value `value`
            Otherwise, returns False.
        """

        for d in self.mydice:
            if d.value == value:
                return True
        return False

    def score(self):
        """Sums up the values of all the dice in the Hand.

        Example:
        if the hand has 4 dice and all of them have the value 2, Return 8
        """

        total = 0
        for d in self.mydice:
            total += d.value
        return total

    def reroll(self, mask):
        """Given a mask, rerolls the die in the hand where the mask
        has a 1

        Example: if the hand has 4 dice,
           - the mask "1000" will reroll only the first die
           - the mask "1111" will reroll all the dice
           - the mask "0000" will reroll none of the dice

        A Die knows how to roll itself. Make use of that instance method.

        Returns True if any dice were rerolled. False if the mask directed
        that no die be rerolled.

        Precondition: mask is a string of exclusively 0s and 1s
                      len(mask) == number of dice in this hand
        """

        if "1" in mask:
            for i in range(0, len(mask)):
                if mask[i] == "1":
                    printer.print_rerolling(i)
                    self.mydice[i].roll()
            printer.print_it(self)
            return True
        return False

    def __str__(self):
        """Returns the string that represents the Hand. The pseudo code will
        help you return something like:
        6, 5, 2, 1, 4
        but ultimately, you'll need to return the ASCII art version that
        will print:
        .-------..-------..-------..-------..-------.
        | O   O || O   O || O     ||       || O   O |
        | O   O ||   O   ||       ||   O   ||       |
        | O   O || O   O ||     O ||       || O   O |
        .-------..-------..-------..-------..-------.
        Note: you should not be typing '|' or 'O' or '_'
        You should look in dice.py to see how to use the pre-set strings.

        To begin with, try something simple that prints out the values of
        each Die. But ultimately, you'll want to print out the ASCII art
        version of the Hand.
        """
        # STUDENTS: Implement this instance method
        mystring = ""
        for i in range(0, dice.Dots.NUM_ROWS):
            one_row = ""
            for one_die in self.mydice:
                one_row += dice.Dots.art[one_die.value][i]
            mystring += one_row + "\n"
        return mystring

    # --------- STUDENTS: Do not change these instance methods ---------

    def initiate_reroll(self):
        # STUDENTS: do not change this function it will be called by a7 code
        printer.prompt_roll(self.get_n_dice())
        mask = self.get_mask()
        return self.reroll(mask)

    def get_mask(self):
        """Prompts the user for a mask. Keeps prompting the
        user until the mask is valid. returns the valid
        Mask. If the user enters the empty string, converts
        this to all 0s. """
        choice = input("Your reroll mask: ")
        while not self.mask_valid(choice):
            choice = input("Your reroll mask: ")
        if choice == "":
            choice = "0"*self.get_n_dice()
        return choice


if __name__ == '__main__':
    n = int(input("How many dice would you like to roll? "))
    hand = Hand(n)
    printer.print_score(hand.score())
    while hand.initiate_reroll():
        printer.print_score(hand.score())

    # an excuse to use contains()
    for i in range(1, dice.Die.NUM_SIDES+1):
        printer.print_tally(i, hand.contains(i))

    # we are nothing if not polite
    printer.print_thanks()
