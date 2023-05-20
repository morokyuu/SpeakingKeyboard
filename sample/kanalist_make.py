


with open("../charlist","r") as fp:
    charlist = [line.rstrip() for line in fp.readlines()]

with open("../hiragana.dat","r") as fp:
    lines = [line.rstrip() for line in fp.readlines()]
    lines = [line.split(' ') for line in lines]
    kanadict = {cols[0]:"./wav/hiragana/"+cols[1] for cols in lines}


for line in charlist:
    key = line[0]
    try:
        print(f"{line} {kanadict[key]}")
    except:
        pass