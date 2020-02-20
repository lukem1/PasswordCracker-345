# PasswordCracker-345
Computer and Network Security Project 1 (Spring 2020: CSCI 345)

## Usage
Running the program:

`python3 main.py [hashfile] [outputfile]`

Hashes are loaded in from the hashfile and output is printed to the outputfile

## Implementation Details

### Multiprocessing
This program implements multiprocessing to speed up password cracking considerably.

The program spawns processes based on the number of available cpu cores on the system.

This works best with the python module `psutil` which is not a part of the standard library. The program
will run with or without the module, but may be slower without it on systems that do not support hyperthreading.  
- When the psutil module is not available the program spawns `(available cpus // 2)` processes (minumum 1).
- When the psutil module is available the program spawns one process for each available hardware cpu core.

#### Multiprocessing vs Multithreading in Python
Due to the [Python Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock) (GIL) multithreaded CPython
programs are unable to fully take advantage of systems with multiple processors.

Multiprocessing bypasses the GIL by creating multiple python instances and allows multiprocessed programs
to fully take advantage of available cpus.

### Wordlist Information
The program uses `/usr/share/dict/words` as the default wordlist

If necessary this can be changed in rules.py (wordlist variable around line 19)
### Testing and Practical Time Analysis
Testing was performed to verify correctness and capabilities as well as inform late stage development decisions. 

Testing was performed on a system with 4 hardware cpu cores and 8 logical cpu cores.

A set of 15 hashes was generated using various passwords that conformed to the rulesets.

The table below shows the time it took the program to crack these hashes with a given number of processes.

This testing was completed before the program was completely optimized and finalized.

After further optimization the completion time with 4 processes has been reduced to approximately `50 seconds`.


| Processes | Time (Seconds) |
| :-------: | :------------: |
|     1     |     437.91     |
|     2     |     237.22     |
|     4     |     154.18     |
|     8     |     172.51     |
