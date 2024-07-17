# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 22:19:40 2024

@author: square
"""

hiragana_label = {
    'a': "あ", 'i': "い", 'u': "う", 'e': "え", 'o': "お", 'ka': "か", 'ki': "き", 'ku': "く", 'ke': "け", 'ko': "こ",
    'sa': "さ", 'si': "し", 'su': "す", 'se': "せ", 'so': "そ", 'ta': "た", 'ti': "ち", 'tu': "つ", 'te': "て",
    'to': "と", 'na': "な", 'ni': "に", 'nu': "ぬ", 'ne': "ね", 'no': "の", 'ha': "は", 'hi': "ひ", 'hu': "ふ",
    'he': "へ", 'ho': "ほ", 'ma': "ま", 'mi': "み", 'mu': "む", 'me': "め", 'mo': "も", 'ya': "や", 'yu': "ゆ",
    'yo': "よ", 'ra': "ら", 'ri': "り", 'ru': "る", 're': "れ", 'ro': "ろ", 'wa': "わ", 'wo': "を", 'nn': "ん",
    '0':"゜",':':"゛",'xtu':"っ",'xya':"ゃ",'xyu':"ゅ",'xyo':"ょ",'nobashi':"ー"
}
katakana_label = {
    'a': "ア", 'i': "イ", 'u': "ウ", 'e': "エ", 'o': "オ", 'ka': "カ", 'ki': "キ", 'ku': "ク", 'ke': "ケ", 'ko': "コ",
    'sa': "サ", 'si': "シ", 'su': "ス", 'se': "セ", 'so': "ソ", 'ta': "タ", 'ti': "チ", 'tu': "ツ", 'te': "テ",
    'to': "ト", 'na': "ナ", 'ni': "ニ", 'nu': "ヌ", 'ne': "ネ", 'no': "ノ", 'ha': "ハ", 'hi': "ヒ", 'hu': "フ",
    'he': "ヘ", 'ho': "ホ", 'ma': "マ", 'mi': "ミ", 'mu': "ム", 'me': "メ", 'mo': "モ", 'ya': "ヤ", 'yu': "ユ",
    'yo': "ヨ", 'ra': "ラ", 'ri': "リ", 'ru': "ル", 're': "レ", 'ro': "ロ", 'wa': "ワ", 'wo': "ヲ", 'nn': "ン",
    '0':"゜",':':"゛",'xtu':"ッ",'xya':"ャ",'xyu':"ュ",'xyo':"ョ",'nobashi':"ー"
}
hira_daku = 'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ'
kana_daku = 'ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ'

daku = dict([(k,h) for k,h in zip(kana_daku,hira_daku)])



kana2hira_dict = dict([(katakana_label[key],hiragana_label[key]) for key in hiragana_label.keys()])
# kana2hira_dict = dict([(k,h) for k,h in zip(katakana_label,hiragana_label)])



