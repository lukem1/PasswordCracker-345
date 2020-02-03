#
# rules.py
# PasswordCracker
#
# Luke M
# 19 January 2020
#

import itertools

# List of all rules that the cracker will use
rules = []

# Alphabets
SPECIALS = ['#', '~', '*', '!']
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Default wordlist
wordlist = "/usr/share/dict/words"


# Function for generating permutations of an alphabet with no repetitions
def permutate(alphabet, maxlen):
    sets = []
    for L in range(0, maxlen):
        for subset in itertools.permutations(alphabet, L):
            s = ""
            for c in subset:
                s += c
            sets.append(s)

    return sets


# The following class provides a template for constructing rules for the password cracker
# Appending a subclass of Rule to the rules array will pass the rule to the program
class Rule:
    NAME = ""
    UPPERBOUND = None  # Maximum sequence number (eg wordlist size or number of combinations)

    # Initialize the rule and move to the lower bound
    def __init__(self, lower):
        self.sequence = 0

    # Return the next password(s) in the sequence and add to the sequence number
    def next(self):
        self.sequence += 1
        raise NotImplementedError

    # Close wordlists and perform other cleanup actions
    def clean(self):
        raise NotImplementedError


# The following class implements all of the wordlist based rules
class Passwordify(Rule):
    NAME = "Passwordify: wordlist based rules"
    UPPERBOUND = 0
    with open(wordlist, "r") as file:
        for line in file:
            UPPERBOUND += 1

    def __init__(self, lower):
        Rule.__init__(self, lower)
        self.list = open(wordlist, 'r')
        for i in range(0, lower):
            self.next()

    def next(self):
        self.sequence += 1

        if self.sequence > self.UPPERBOUND:
            return None

        word = self.list.readline().replace("\n", "")

        passwords = []
        if len(word) == 7:
            base = word[0].upper() + word[1:]

            for i in range(0, 10):
                passwords.append(base + str(i))

            return passwords
        elif len(word) == 5:
            return [word.replace('a', '@').replace('l', '1')]
        else:
            return [word]

    def clean(self):
        self.list.close()


rules.append(Passwordify)


# The following class is used to help generate permutations of an alphabet
class Stepper:
    def __init__(self, alphabet):
        self.next = None
        self.counter = -1
        self.alphabet = alphabet
        self.value = ''

    def step(self):
        self.counter += 1
        if self.counter == len(self.alphabet):
            self.counter = 0
            if self.next is not None:
                self.next.step()
        self.value = self.alphabet[self.counter]

    def build(self):
        if self.next is not None:
            return self.next.build() + self.value
        return self.value


# The following class implements the 5 digit code  with special characters rule
class Combinations1(Rule):
    NAME = "Combinations1: special chars + 5 digit code"
    UPPERBOUND = 99999

    def __init__(self, lower):
        Rule.__init__(self, lower)
        self.sequence = lower

    def next(self):
        base = "%05d" % self.sequence
        codes = [base]
        perms = permutate(SPECIALS, len(SPECIALS)+1)
        perms.remove("")

        for p in perms:
            codes.append(p+base)

        self.sequence += 1
        return codes

    def clean(self):
        pass  # No cleaning required


rules.append(Combinations1)


# The following class implements the up to 7 digit code rule
class Combinations2(Rule):
    NAME = "Combinations2: <= 7 Digit Codes"
    UPPERBOUND = 11111110

    def __init__(self, lower):
        Rule.__init__(self, lower)
        self.steppers = Stepper(DIGITS)
        self.sequence = 0
        cstepper = self.steppers
        for i in range(0, 6):
            cstepper.next = Stepper(DIGITS)
            cstepper = cstepper.next

        for i in range(0, lower):
            self.next()

    def next(self):
        self.steppers.step()
        return [self.steppers.build()]

    def clean(self):
        pass  # No cleaning required


rules.append(Combinations2)
