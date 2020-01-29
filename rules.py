#
# rules.py
# PasswordCracker
#
# Luke M
# 19 January 2020
#

rules = []
wordlist = "/usr/share/dict/words"

class Rule():
    sequence = 0
    upperBound = None

    # Initialize the rule and move to the lower bound
    def __init__(self, lower, upper):
        self.upperBound = upper

        for i in range(0, lower):
            self.next()

    # Return the next password(s) in the sequence and add to the sequence number
    def next(self):
        self.sequence += 1
        raise NotImplementedError

    # Close wordlists and perform other cleanup actions
    def clean(self):
        raise NotImplementedError


class Passwordify1(Rule):
    list = open(wordlist)

    def next(self):
        self.sequence += 1

        if self.sequence > self.upperBound:
            return None

        word = self.list.readline().replace("\n", "")

        if len(word) != 7:
            return []

        passwords = []

        base = word[0].upper() + word[1:]

        for i in range(0, 10):
            passwords.append(base + str(i))

        return passwords

    def clean(self):
        self.list.close()
