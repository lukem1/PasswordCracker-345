#
# cracker.py
# PasswordCracker
#
# Luke M
# 21 January 2020
#

import hashlib
import multiprocessing
from rules import *


class Hash():

    def __init__(self, value, username=""):
        self.value = value
        self.username = username
        self.cracked = False
        self.password = None

    def guess(self, password):
        if calc_hash(password) == self.value:
            self.cracked = True
            self.password = password
            print("%s:%s    (%s)" % (self.value, self.password, self.username))
            return True
        else:
            return False


def crack(bounds, hashes):
    print("Starting")
    for r in rules:
        lower, upper = bounds
        nr = r(lower, upper)
        for i in range(lower, upper):

            if len(hashes) == 0:
                return
            guesses = nr.next()
            for g in guesses:
                for h in hashes:
                    h.guess(g)

    print("Ending")

# Calculate and return the 256 bit shasum of a password
def calc_hash(password):
    return hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest()

