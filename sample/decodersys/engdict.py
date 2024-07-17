# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 20:53:37 2024

@author: square
"""

import string

eng = string.ascii_lowercase
letter = dict([(e,e) for e in eng])


num = """zero
one
two
three
four
five
six
seven
eight
nine
ten"""
numname = num.split('\n')
number = dict([(digit,name) for digit,name in zip(string.digits,numname)])

mojidict = letter | number

print(mojidict)