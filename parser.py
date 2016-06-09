#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

if len(sys.argv) < 3:
	print >> sys.stderr, "Usage:", sys.argv[0], "extension-list file-list"
	print >> sys.stderr, "  Example:", sys.argv[0], "es,com,de file1.txt file2.txt"
	sys.exit(0)

special_chars = "áàèéíóòúäëïöüñ"

extensions = sys.argv[1].split(",")
matchers = [ re.compile("^[" + special_chars + "a-z0-9\-]+\."+ext.replace(".", "\.")+"$") for ext in extensions ]

for f in sys.argv[2:]:
	c = open(f,"rb").read()
	for line in c.split("\n"):
		for m in matchers:
			res = m.search(line)
			if res:
				print res.group()


