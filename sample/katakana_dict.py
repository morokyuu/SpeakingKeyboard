import jaconv

moto = """
        before = 'かきくけこさしすせそたちつてとはひふへほ'
        after = 'がぎぐげござじずぜぞだぢづでどばびぶべぼ'


        before = 'はひふへほ'
        after = 'ぱぴぷぺぽ'
"""

ch = jaconv.hira2kata(moto)

print(ch)




