#!/bin/bash

mkdir -p results
mkdir tmp.fr/
cd    tmp.fr/

# Get all GIF images
../fr.download.py

cd ../

for file in tmp.fr/*
do
	./frcrawl.py $file >> tmp.fr/all.txt
done

cat tmp.fr/all.txt | sort | uniq | gzip -9 > results/dot.fr.txt.gz

rm -rf tmp.fr

