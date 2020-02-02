# PasswordCracker-345
Computer and Network Security Project 1 (Spring 2020: CSCI 345)

## Usage
Running the program:

`python3 main.py [hashfile] [outputfile]`

Hashes are loaded in from the hashfile and output is printed to the outputfile

## Implementation Details

### Multiprocessing
The program spawns available cpus // 2 processes and splits the work between them.
Testing showed that that was the optimal number of processes.
### Wordlist Information
The program uses `/usr/share/dict/words` as the default wordlist
### Testing and Practical Time Analysis
Testing was done with a set of 15 hashes of passwords that followed the rules.
Before optimization, the program took approximately 150 seconds to crack all 15 hashes.

| Processes | Time (Seconds) |
| :-------: | :------------: |
|     1     |     437.91     |
|     2     |     237.22     |
|     4     |     154.18     |
|     8     |     172.51     |
