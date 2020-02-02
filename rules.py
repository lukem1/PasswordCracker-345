#
# rules.py
# PasswordCracker
#
# Luke M
# 19 January 2020
#

import itertools

rules = []
wordlist = "/usr/share/dict/words"


class Rule:
    upperBound = None  # Maximum sequence number (eg wordlist size or number of combinations)

    # Initialize the rule and move to the lower bound
    def __init__(self, lower, upper):
        self.sequence = 0

    # Return the next password(s) in the sequence and add to the sequence number
    def next(self):
        self.sequence += 1
        raise NotImplementedError

    # Close wordlists and perform other cleanup actions
    def clean(self):
        raise NotImplementedError


class Passwordify(Rule):
    UPPERBOUND = 0
    with open(wordlist, "r") as file:
        for line in file:
            UPPERBOUND += 1

    def __init__(self, lower, upper):
        Rule.__init__(self, lower, upper)
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


class Combinations1(Rule):
    UPPERBOUND = 99999

    def __init__(self, lower, upper):
        Rule.__init__(self, lower, upper)
        self.sequence = lower

    def next(self):
        base = "%05d" % self.sequence
        codes = [base]
        specials = "*~!#"
        perms = ["".join(x) for x in itertools.chain.from_iterable(itertools.permutations(specials, i + 1) for i in range(0, len(specials)))]

        for p in perms:
            codes.append(p+base)

        self.sequence += 1
        return codes

    def clean(self):
        pass  # No cleaning required


rules.append(Combinations1)
