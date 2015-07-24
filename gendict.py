#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

outfile = sys.argv[1]
extensions = sys.argv[2].split(",")
files = sys.argv[3:]

of = open(outfile, "a")

words = set()
for f in files:
	print "Reading", f, "..."
	filec = open(f,"rb").read()
	words.update(filec.split("\n"))

words = list(words)

replacements = [
	("ü", "u"), ("é", "e"), ("â", "a"),
	("ä", "a"), ("à", "a"), ("å", "a"),
	("ç", "c"), ("ê", "e"), ("ë", "e"),
	("è", "e"), ("ï", "i"), ("î", "i"),
	("ì", "i"), ("ï", "i"), ("î", "i"),
	("ô", "o"), ("ö", "o"), ("ò", "o"),
	("û", "u"), ("ù", "u"), ("ÿ", "y"),
	("á", "a"), ("í", "i"), ("ó", "o"),
	("ñ", "n"), ("¢", "c"),
]

def mangle(w):
	w = w.split("/")[0]
	nw = w
	for r in replacements:
		nw = nw.replace(r[0], r[1])

	if nw != w:
		yield nw
	yield w

for ext in extensions:
	for w in words:
		for mangw in mangle(w.lower()):
			of.write("%s.%s\n" % (mangw, ext))



