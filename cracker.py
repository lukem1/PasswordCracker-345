#
# cracker.py
# PasswordCracker
#
# Luke M
# 21 January 2020
#

import hashlib
import threading
import time

# TODO: kill related threads when a thread cracks a password
class Cracker(threading.Thread):
    def __init__(self, threadID, generator):
        threading.Thread.__init__(self)
        self.name = "Thread " + str(threadID)
        self.threadID = threadID
        self.generator = generator

    def run(self):
        print("Starting " + self.name)
        for i in range(0, 2*self.threadID):
            print("Thread %s execution %d" % (self.threadID, i))
            time.sleep(1)
        print("Exiting " + self.name)


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
