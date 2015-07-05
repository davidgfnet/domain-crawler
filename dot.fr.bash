#!/bin/bash

mkdir -p results
mkdir tmp.fr/
cd    tmp.fr/

wget -l 1  --no-directories -A gif -r  "http://www.afnic.fr/data/divers/public/publication-quotidienne-img/"

cd ../

for file in tmp.fr/*
do
	./frcrawl.py $file >> tmp.fr/all.txt
done

cat tmp.fr/all.txt | sort | uniq | gzip -9 > results/dot.fr.txt.gz

rm -rf tmp.fr

