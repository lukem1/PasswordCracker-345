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


# Load in hashes from a file
def load_hashes(file):
    hashes = []
    data = None
    with open(file, 'r') as file:
        data = file.readlines()

    try:
        count = 0
        for line in data:
            if line == "":
                break
            line = line.replace('\n', '')
            line = line.split(":")
            hashes.append(Hash(line[1], count, line[0]))
            count += 1

    except:
        print("Error reading in hashes\nCheck to make sure the hashfile is properly formatted")
        exit(-1)

    return hashes


def main():
    hashes = []

    if len(sys.argv) <= 1:
        print("Usage: python3 main.py <hashfile> <outfile>")
        return
    elif len(sys.argv) == 3:
        hashfile = sys.argv[1]
        outfile = sys.argv[2]
        try:
            hashes = load_hashes(hashfile)
        except IOError:
            print("Error: Unable to read hash file (%s)" % hashfile)
            return

        try:
            outStream = open(outfile, "w+")
            outStream.close()
        except IOError:
            print("Error: Unable to create output file (%s)" % outfile)
            return

    lines = 0
    with open(wordlist, "r") as file:
        for line in file:
            lines += 1

    hashLock = multiprocessing.Lock()
    hashStatus = multiprocessing.Array('i', [0]*len(hashes))

    print("Wordlist length: " + str(lines))
    print("Available CPUs: %d" % CPUCOUNT)
    print("Creating %d processes..." % CPUCOUNT)
    start = time.time()
    procs = []
    for i in range(1, CPUCOUNT+1):
        p = multiprocessing.Process(target=crack, args=(hashes, hashStatus, hashLock, CPUCOUNT, i, outfile))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

    end = time.time()
    print("All processes have completed.")

    # Aggregate data and print summary info
    outHashes = []
    data = None
    with open(outfile, 'r') as file:
        data = file.readlines()

    count = 0
    for line in data:
        line = line.split(":")
        h = Hash(line[0], count, "")
        h.password = line[1].replace('\n', '')
        outHashes.append(h)
        count += 1

    hashCount = len(hashStatus)
    crackedCount = 0
    for h in hashStatus:
        if h == 1:
            crackedCount += 1

    for h in hashes:
        if hashStatus[h.id] == 1:
            h.cracked = True

        for o in outHashes:
            if h.value == o.value:
                o.cracked = h.cracked
                o.username = h.username
                break

    print("------------------Summary------------------")
    print("Cracked %d/%d hashes in %.5f seconds" % (crackedCount, hashCount, (end-start)))
    for o in outHashes:
        if o.cracked:
            print("%s:%s    (%s)" % (o.value, o.password, o.username))


if __name__ == "__main__":
    main()
