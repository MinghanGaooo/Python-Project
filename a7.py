# a7.py
# Minghan Gao (mg2328), Sheila Yu (sy552)
# Sources/people consulted: John Rubio
# May 6, 2023
# Skeleton by Prof. Bracy, AWB93, April, 2023

import dice, a6

class Rules():
    """A class to store some of the basic assumptions and rules of the game."""

    NUM_DICE = 5

    # numbers for each of the 13 categories
    CHANCE = 0
    ONES = 1
    TWOS = 2
    THREES = 3
    FOURS = 4
    FIVES = 5
    SIXES = 6
    THREE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 9
    SM_STRAIGHT = 10
    LG_STRAIGHT = 11
    YAHTZEE = 12
    NUM_CATEGORIES = 13

    """
    Remember it is bad form to have `magic numbers` in your code.  Instead,
    you can create a variable whose name offers a meaningful description of
    what that number is. Here are some constants below that we want you to use.
    """
    FULL_HOUSE_PTS = 25
    SM_STRAIGHT_PTS = 30
    LG_STRAIGHT_PTS = 40
    YAHTZEE_PTS = 50

    names = ["Chance", "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",\
             "3 of a kind", "4 of a kind", "Full House", "Small Straight",\
             "Large Straight", "Yahtzee (5x!)"]

    descriptions = [" -- sum all 5 dice ",
                    "   -- sum 1s only    ",
                    "   -- sum 2s only    ",
                    " -- sum 3s only    ",
                    "  -- sum 4s only    ",
                    "  -- sum 5s only    ",
                    "  -- sum 6s only    ",
                    " -- sum all 5 ",
                    " -- sum all 5 ",
                    "     -- "+str(FULL_HOUSE_PTS)+" pts ",
                    " -- "+str(SM_STRAIGHT_PTS)+" pts",
                    " -- "+str(LG_STRAIGHT_PTS)+" pts",
                    "  -- "+str(YAHTZEE_PTS)+" pts"]

class Basic():
    """Basic is the simplest way to score a hand in Yahtzee.
    Any 5-dice hand meets the criteria to count for Basic.
    The score is the sum of the values of all the dice in the hand.
    """

    def __init__(self, index):
        """Creates an instance of a Basic with the following attributes:

        index:      [int] which scorecard entry this is associated with
        is_filled:  [bool] whether a hand has been assigned to this Basic
                    (this is always False in the beginning)
        points:     [int] once a hand as been associated with this category,
                    the points attribute will reflect the score
        max_points: [int] the best score one can get with this category. this
                    field will be used for the scoreboard to let users know
                    how many points they stand to earn under this category

        Precondition: 0 <= index [int] <= Rules.YAHTZEE
        """
        assert index >= 0, "index must be a positive integer"
        assert index <= Rules.YAHTZEE, \
            "index must be no larger than"+str(Rules.YAHTZEE)
        self.index = index
        self.is_filled = False
        self.points = 0
        self.max_points = Rules.NUM_DICE * dice.Die.NUM_SIDES

    def score(self, hand):
        """When Basic is scored, simply sum the value of all dice in the hand.
        Also mark the category as filled. Each category can only be used once.
        """
        self.points = hand.score()
        self.is_filled = True

    def __str__(self):
        """This method should be sufficient for this class and any of its
        subclasses."""
        end = "/"+str(self.max_points)+"]"
        if not self.is_filled:
            scoretext = " [ "+end
        else:
            scoretext = " ["+str(self.points)+end
        return str(self.index) + ": "+ Rules.names[self.index]+\
            Rules.descriptions[self.index] + scoretext

class OneToSix(Basic):
    def __init__(self, index):
        super().__init__(index)
        self.max_points = self.index * Rules.NUM_DICE

    def score(self, hand):
        dice = hand.get_dice()
        for i in dice:
            if i.value == self.index:
                self.points += i.value
        self.is_filled = True

class OfAKind(Basic):
    def __init__(self, index, s):
        super().__init__(index)
        self.s = s
        if s == 12:
            self.max_points = Rules.YAHTZEE_PTS

    def score(self, hand):
        dice = hand.get_dice()
        value = []
        for i in dice:
            value.append(i.value)
            for j in value:
                if value.count(j) >= 3 and self.s == 7:
                    self.points = hand.score()
                if value.count(j) >= 4 and self.s == 8:
                    self.points = hand.score()
                if value.count(j) == 5 and self.s == 12:
                    self.points = Rules.YAHTZEE_PTS
        self.is_filled = True

class FullHouse(Basic):
    def __init__(self, index):
        super().__init__(index)
        self.max_points = Rules.FULL_HOUSE_PTS

    def score(self, hand):
        dice = hand.get_dice()
        value = []
        accum = []
        times = []
        for i in dice:
            value.append(i.value)
            if i.value not in accum:
                accum.append(i.value)
        for j in accum:
            times.append(value.count(j))
        if 3 in times and 2 in times:
            self.points = self.max_points
        self.is_filled = True

class Straight(Basic):
    def __init__(self, index, s):
        super().__init__(index)
        self.s = s
        if s == 10:
            self.max_points = Rules.SM_STRAIGHT_PTS
        if s == 11:
            self.max_points = Rules.LG_STRAIGHT_PTS

    def score(self, hand):
        dice = hand.get_dice()
        value = []
        for i in dice:
            value.append(i.value)
        value.sort()
        i = 0
        count = 0
        while i < len(value) - 1:
            if value[i] == value[i+1] - 1:
                count += 1
            i += 1
        if count >= 3 and self.s == 10:
            self.points = self.max_points
        if count == 4 and self.s == 11:
            self.points = self.max_points
        self.is_filled = True


class Scorecard():
    """The scorecard tells you what categories there are, what points can be
    earned, which ones have been filled, and what your total score is so far.
    """

    def __init__(self):
        """
        Instance attributes:
          total_score: [int] tells you how  many points have been earned
          categories: [list of Basic] there are 13 categories in the game
                  and this list keeps track of each of them
        """
        self.total_score = 0
        self.categories = [None]*Rules.NUM_CATEGORIES
        self.categories[Rules.CHANCE] = Basic(Rules.CHANCE)
        self.categories[Rules.ONES] = OneToSix(Rules.ONES)
        self.categories[Rules.TWOS] = OneToSix(Rules.TWOS)
        self.categories[Rules.THREES] = OneToSix(Rules.THREES)
        self.categories[Rules.FOURS] = OneToSix(Rules.FOURS)
        self.categories[Rules.FIVES] = OneToSix(Rules.FIVES)
        self.categories[Rules.SIXES] = OneToSix(Rules.SIXES)
        self.categories[Rules.THREE_OF_A_KIND] = OfAKind(Rules.THREE_OF_A_KIND, 7)
        self.categories[Rules.FOUR_OF_A_KIND] = OfAKind(Rules.FOUR_OF_A_KIND, 8)
        self.categories[Rules.FULL_HOUSE] = FullHouse(Rules.FULL_HOUSE)
        self.categories[Rules.SM_STRAIGHT] = Straight(Rules.SM_STRAIGHT, 10)
        self.categories[Rules.LG_STRAIGHT] = Straight(Rules.LG_STRAIGHT, 11)
        self.categories[Rules.YAHTZEE] = OfAKind(Rules.YAHTZEE, 12)

    # --------- STUDENTS: Do not modify any of the code below ---------


    def cat_prompt(self):
        print(self)
        print("How would you like to categorize these dice?")

    def set_hand(self, hand, choice):
        """Associates a hand with one of the game categories."""
        self.categories[choice].score(hand)
        s = self.categories[choice].points
        print("You just earned "+str(s)+" points!\n")
        self.total_score += s

    def __str__(self):
        """Prints out the scorecard, one category (row) at a time."""
        result = ""
        for c in self.categories:
            result += str(c)+"\n"
        return result

    def choice_okay(self, choice):
        """
        Makes the game more usable by not letting the user select a category
        that has already been chosen or that is not valid.
        """
        if not choice.isnumeric():
            print("Please enter a number.")
            return False
        choice = int(choice)
        if (choice < 0):
            print("category index must be a positive integer.")
            return False
        if (choice > Rules.YAHTZEE):
            print("The largest category index in Yahtzee is "+str(Rules.YAHTZEE))
            return False
        if (self.categories[choice] == None):
            print("This category has not been implemented yet.")
            return False
        if (self.categories[choice].is_filled):
            print("That category has already been filled.")
            return False
        return True

    def get_choice(self):
        """Prompts the user to pick a category that they wish apply
        their current hand to.
        """
        choice = input("Your choice: ")
        while(not self.choice_okay(choice)):
            choice = input("Your choice: ")
        return int(choice)

def get_hand():
    """Rolls the dice and allows the user to re-roll up to 2 more times."""
    print("Rolling the dice...")
    hand = a6.Hand(Rules.NUM_DICE)
    if hand.initiate_reroll():
        hand.initiate_reroll()
    return hand

if __name__=='__main__':
    sc = Scorecard()
    print("Welcome to Yahtzee!")
    print(sc)
    n_turns = Rules.NUM_CATEGORIES - sc.categories.count(None)

    while (n_turns > 0):
        print("You have "+str(n_turns)+" rolls left.")
        hand = get_hand()
        sc.cat_prompt()
        choice = sc.get_choice()
        sc.set_hand(hand, choice)
        print(sc)
        print("Current score = "+str(sc.total_score))
        print("--------------------------------------------")
        n_turns -= 1

    print("FINAL SCORE = "+str(sc.total_score)+"\nThanks for playing!")
