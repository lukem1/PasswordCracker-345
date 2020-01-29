#
# cracker.py
# PasswordCracker
#
# Luke M
# 21 January 2020
#

import hashlib
from rules import rules
def crack(bounds, hashes):
    pass

# Calculate and return the 256 bit shasum of a password
def calc_hash(password):
    return hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest()


# Read hashes from file and return as list of (username, hash) tuples
def read_hashes(file):
    hashes = []
    with open(file, "r") as file:
        for line in file:
            line = line.split(":")
            hashes.append((line[0], line[1]))

    return hashes
