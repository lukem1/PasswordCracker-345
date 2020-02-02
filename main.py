#
# main.py
# PasswordCracker
#
# Luke M
# 19 January 2020
#

from cracker import *
import hashlib
from rules import *
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
    count = 0
    for line in data:
        line = line.split(":")
        hashes.append(Hash(line[1], count, line[0]))
        count += 1

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

    if multiprocessing.cpu_count() == 1:
        procCount = 1
    else:
        procCount = multiprocessing.cpu_count() // 2

    hashLock = multiprocessing.Lock()
    hashStatus = multiprocessing.Array('i', [0]*len(hashes))

    test = Combinations2(0, Combinations2.UPPERBOUND)
    print(Combinations2.UPPERBOUND)
    #for i in range(0, Combinations2.UPPERBOUND):
     #   print(test.next())

    print("Wordlist length: " + str(lines))
    print("Available CPUs: %d" % (multiprocessing.cpu_count()))
    print("Creating %d processes..." % procCount)
    start = time.time()
    procs = []
    for i in range(1, procCount+1):
        p = multiprocessing.Process(target=crack, args=(hashes, hashStatus, hashLock, procCount, i))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

    end = time.time()
    print(hashStatus[:])
    print("Time: %.20f seconds" % (end - start))



if __name__ == "__main__":
    main()
