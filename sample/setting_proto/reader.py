import sys

#filename = sys.argv[1]
#filename = "pairfile.txt"
filename = "../../hiragana.dat"

with open(filename,"r") as fp:
    pairs = [line.rstrip().split(' ') for line in fp.readlines()]

print(pairs)
