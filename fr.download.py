#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, re
p = re.compile(ur'href="(/data/divers/public/publication-quotidienne/[^\.]+\.gif)"', re.MULTILINE)

response = urllib.urlopen('https://www.afnic.fr/fr/produits-et-services/services/liste-quotidienne-des-noms-de-domaine-enregistres/')
html = response.read()

# Get GIFs in /data/divers/public/publication-quotidienne/*.gif
for img in re.findall(p, html):
	url = 'https://www.afnic.fr%s' % img
	bn = url.split("/")[-1]
	open(bn, "wb").write(urllib.urlopen(url).read())


