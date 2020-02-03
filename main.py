#
# main.py
# PasswordCracker
#
# Luke M
# 19 January 2020
#

from cracker import *
import multiprocessing
from rules import *
import sys
import time

CPUCOUNT = 0
try:
    import psutil
    CPUCOUNT = psutil.cpu_count(logical=False)
except ImportError:
    print("!!! for improved multiprocessing performance install the psutil module for python")
    c = multiprocessing.cpu_count()
    if c == 1:
        CPUCOUNT = 1
    else:
        CPUCOUNT = c // 2

def print_writer(data, file):
    print(data)
    file.write(data + "\n")


# Load in hashes from a file
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
            print("Error: Unable to read hash file (%s)" % hashFile)
            return

        try:
            outStream = open(outFile, "w+")
        except IOError:
            print("Error: Unable to create output file (%s)" % outFile)
            return

    lines = 0
    with open(wordlist, "r") as file:
        for line in file:
            lines += 1

    hashLock = multiprocessing.Lock()
    hashStatus = multiprocessing.Array('i', [0]*len(hashes))

    print("Wordlist length: " + str(lines))
    print("Available CPUs: %d" % (multiprocessing.cpu_count()))
    print("Creating %d processes..." % CPUCOUNT)
    start = time.time()
    procs = []
    for i in range(1, CPUCOUNT+1):
        p = multiprocessing.Process(target=crack, args=(hashes, hashStatus, hashLock, CPUCOUNT, i))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

    end = time.time()
    print(hashStatus[:])
    print("Time: %.20f seconds" % (end - start))


if __name__ == "__main__":
    main()
