# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:50:18 2024

@author: square
"""

import csv

with open('words.csv') as f:
    # print(f.read())
    reader = csv.reader(f)
    for row in reader:
        print(row)