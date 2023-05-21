


with open("../midashi","r") as fp:
    midashi = [line.rstrip() for line in fp.readlines()]

with open("../kana_number.txt","r") as fp:
    lines = [line.rstrip() for line in fp.readlines()]
    lines = [line.split(' ') for line in lines]
    kanadict = {cols[2]:cols for cols in lines}


for m in midashi:
    try:
        print(f"{kanadict[m][1]} {kanadict[m][0]}")
    except:
        pass
