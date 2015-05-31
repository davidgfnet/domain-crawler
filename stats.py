#!/bin/python

import sys

c = open(sys.argv[1],"rb").read()

lengths = {}
for dom in c.split("\n"):
	s = len(dom)
	if s not in lengths: lengths[s] = 0
	lengths[s] += 1

of = open(sys.argv[1]+".csv","wb")
for s in sorted(list(lengths.keys())):
	of.write(str(s) + "," + str(lengths[s]) + "\n")

