# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 23:00:05 2024

@author: square
"""

import sqlite3

with sqlite3.connect('tango.db') as conn:
    cur = conn.cursor()
    cur.execute('select * from sample')
    for row in cur:
        print(row)
