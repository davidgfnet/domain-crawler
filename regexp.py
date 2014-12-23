#!/usr/bin/env python
import re,sys

r = re.findall(sys.argv[1], sys.stdin.read())
for e in r:
	print e

