#!/usr/bin/env python

import sys
import re

if len(sys.argv) < 3:
	print >> sys.stderr, "Usage:", sys.argv[0], "extension-list file-list"
	print >> sys.stderr, "  Example:", sys.argv[0], "es,com,de file1.txt file2.txt"
	sys.exit(0)

extensions = sys.argv[1].split(",")
matchers = [ re.compile("[a-z]+[a-z0-9\-]*\."+ext) for ext in extensions ]

for f in sys.argv[2:]:
	c = open(f,"rb").read()
	for line in c.split("\n"):
		for m in matchers:
			res = m.search(line)
			if res:
				print res.group()


