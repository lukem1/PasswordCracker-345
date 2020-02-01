#
# main.py
# PasswordCracker
#
# Luke M
# 19 January 2020
#

from cracker import *
import hashlib
from rules import Passwordify1, wordlist
import sys
import multiprocessing
import time


def print_writer(data, file):
    print(data)
    file.write(data + "\n")

def load_hashes(file):
    hashes = []
    data = None
    with open(file, 'r') as file:
        data = file.readlines()

    #try:
    for line in data:
        line = line.split(":")
        hashes.append(Hash(line[1], line[0]))

    #except:
        #print("Error reading in hashes")

    return hashes


def main():
    hashes = []
    hashFile = ""
    outFile = ""
    outStream = None

    if len(sys.argv) <= 1:
        print("Usage: python3 main.py <hashfile> <outfile>")
    elif len(sys.argv) == 3:
        print("Loading parameter settings...")
        hashFile = sys.argv[1]
        outFile = sys.argv[2]
        try:
            hashes = load_hashes(hashFile)
        except IOError:
            print("Error: Unable to read hash file (%s)" % (hashFile))
            return

        try:
            outStream = open(outFile, "w+")
        except IOError:
            print("Error: Unable to create output file (%s)" % (outFile))
            return

    lines = 0
    with open(wordlist, "r") as file:
        for line in file:
            lines += 1

        print("Wordlist length: " + str(lines))

    p1 = multiprocessing.Process(target=crack, args=((0, lines), hashes))
    start = time.time()
    p1.start()
    p1.join()
    end = time.time()

    print("Time: %.20f seconds" % (end - start))



if __name__ == "__main__":
    main()
