import sys

#filename = sys.argv[1]
filename = "pairfile.txt"

with open(filename,"r") as fp:
    lines = [line.rstrip() for line in fp.readlines()]

print(lines)
