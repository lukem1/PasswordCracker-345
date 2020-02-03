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


class Hash:

    def __init__(self, value, id, username=""):
        self.value = value
        self.id = id
        self.username = username
        self.cracked = False
        self.password = None

    def guess(self, password, hashStat, hashLock):
        if not self.cracked:
            if calc_hash(password) == self.value:
                hashLock.acquire()
                hashStat[self.id] = 1
                hashLock.release()
                self.cracked = True
                self.password = password
                print("%s:%s    (%s)" % (self.value, self.password, self.username))
                return True
            else:
                return False
        else:
            return False


def crack(hashes, hashStat, hashLock, procCount, procID):
    print("Started Process %d" % procID)
    for r in rules:
        step = r.UPPERBOUND//procCount
        lower = step*(procID-1)
        if procCount == procID:
            upper = r.UPPERBOUND
        else:
            upper = step*procID
        gen = r(lower)
        print("Range info:: Current: %d-%d, Available: %d-%d" % (lower, upper, 0, r.UPPERBOUND))
        statCount = 0
        for i in range(lower, upper):
            statCount += 1
            if statCount == (1000+procID):  # procID addition to induce variation between processes
                statCount = 0
                #print("Progress: %d/%d" % (i, upper))
                hashLock.acquire()
                done = True
                for h in hashes:
                    if not h.cracked:
                        status = hashStat[h.id]
                        if status == 1:
                            h.cracked = True
                        else:
                            done = False
                hashLock.release()
                if done:
                    return

            guesses = gen.next()
            for g in guesses:
                for h in hashes:
                    h.guess(g, hashStat, hashLock)
        gen.clean()

    print("Ended Process %d" % procID)


# Calculate and return the 256 bit shasum of a password
def calc_hash(password):
    return hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest()

