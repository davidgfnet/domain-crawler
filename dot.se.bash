#!/bin/bash

mkdir -p results/

wget -O - "https://www.iis.se/data/bardate_domains.txt" | cut -f 1 | gzip -9 > results/dot.se.txt.gz


