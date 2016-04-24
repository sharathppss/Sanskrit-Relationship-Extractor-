#!/usr/bin/python2.7 -tt

import re
import sys

fd = open (sys.argv[1], "r")
out_file = sys.argv[1]+".out"
fw = open (out_file, "w")

corpus=""
count=0
for line in fd:
    corpus += line
    if "SanSloka" in line:
        word = fd.next()
        if not word[0].isalpha():
            temp = word.split("<")
            fw.write(temp[0] + "\n")

        word = fd.next()
        if not word[0].isalpha():
            temp = word.split("<")
            fw.write(temp[0] + "\n")

        word = fd.next()
        if not word[0].isalpha():
            temp = word.split("<")
            fw.write(temp[0] + "\n")

        word = fd.next()
        if not word[0].isalpha():
            temp = word.split("<")
            fw.write(temp[0] + "\n")
