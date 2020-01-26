#
# rules.py
# PasswordCracker
#
# Luke M
# 19 January 2020
#

# Note: The classes in this file are not meant to be initialized.
# They are meant to provide an easy way to develop generators and rulesets.
# TODO: Shift to a "generator" based design
# TODO: Remove or revise comments
# The following class provides a template for the creation of generators which can be used to generate password guesses
# To create a generator a subclass should be made which modifies the generate method

# The following class provides a template for the creation of rulesets for reading in passwords from wordlists
# To create a ruleset a subclass should be made which modifies the process method
def func1():
    print("one")

def func2():
    print("two")

funcs = [func1, func2]

class Rule():
    name = "name of rule"
    description = "description of rule"

    # Receives the next word from the wordlist and applies the ruleset.
    # Returns a list of generated passwords, if none are generated return an empty list.
    def process(word):
        return [word]

    def getInfo(self):
        return self.name, self.description

# Rule Definitions

# 7 char word, first letter capitalized and a 1-digit number appended.

class Passwordify1(Rule):

    def process(word):
        if len(word) != 7:
            return []

        passwords = []

        base = word[0].upper() + word[1:]

        for i in range(0, 10):
            passwords.append(base+str(i))

        return passwords
