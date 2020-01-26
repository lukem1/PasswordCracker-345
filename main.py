#
# main.py
# PasswordCracker
#
# Luke M
# 19 January 2020
#

from cracker import *
import hashlib
from rules import Passwordify1, funcs
import sys
import time


h = "Puzzles4"
print(hashlib.sha256(bytes(h, encoding="utf-8")).hexdigest())

print(__name__)

t1 = Cracker(0, 1)
t2 = Cracker(1, 2)

t1.start()
t2.start()

for f in funcs:
    f()

def test_gen(sequence):
    alpha = ["", "0", "1", "2", "3", "4", "5"]
    guess = ""
    l = 4
    for i in range(0, l):
        guess = alpha[(sequence % len(alpha))] + guess
        sequence // len(alpha)

    print(guess)

for i in range(0, 50):
    test_gen(i)


def print_writer(data, file):
    print(data)
    file.write(data + "\n")


def main():
    hashes = []
    hashFile = ""
    outFile = ""
    outStream = None

    if len(sys.argv) <= 1:
        print("Usage: python3 main.py <hashfile> <outfile>")
    elif len(sys.argv) == 3:
        hashFile = sys.argv[1]
        outFile = sys.argv[2]
        try:
            hashes = read_hashes(hashFile)
        except IOError:
            print("Error: Unable to read hash file (%s)" % (hashFile))
            return

        try:
            outStream = open(outFile, "w+")
        except IOError:
            print("Error: Unable to create output file (%s)" % (outFile))
            return

        print_writer("hello world!", outStream)

    print(Passwordify1.process("abcdefg"))

if __name__ == "__main__":
    main()