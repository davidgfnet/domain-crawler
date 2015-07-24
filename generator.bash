#!/bin/bash

BP=`pwd`

mkdir -p results-gen/
rm -rf tmp.generated/
mkdir tmp.generated/
cd    tmp.generated/

git clone --depth=1 https://github.com/titoBouzout/Dictionaries.git

cd Dictionaries

$BP/gendict.py "domains.txt" eus "Basque.dic"
$BP/gendict.py "domains.txt" bg "Bulgarian.dic"
$BP/gendict.py "domains.txt" "es,cat" "Catalan.dic"
$BP/gendict.py "domains.txt" hr "Croatian.dic"
$BP/gendict.py "domains.txt" cz "Czech.dic"
$BP/gendict.py "domains.txt" dk "Danish.dic"
$BP/gendict.py "domains.txt" nl "Dutch.dic"
$BP/gendict.py "domains.txt" "uk,us,au,nz,co.nz,co.uk,in,pk,ph,de,ca,fr,it,th,pl,es,cn,bd,gi,im,ie,jm,ch" "English (American).dic" "English (Australian).dic" "English (British).dic" "English (Canadian).dic" "English (South African).dic"
$BP/gendict.py "domains.txt" "lu,fr,re,tf,ch" "French.dic"
$BP/gendict.py "domains.txt" gal "Galego.dic"
$BP/gendict.py "domains.txt" "at,de,ch" "German.dic"

$BP/gendict.py "domains.txt" it "Italian.dic"
$BP/gendict.py "domains.txt" "pt,br" "Portuguese (European).dic" "Portuguese (Brazilian).dic"
$BP/gendict.py "domains.txt" "es,com.es" "Spanish.dic"
$BP/gendict.py "domains.txt" "se" "Swedish.dic"

cd ..

$BP/digger/digger < Dictionaries/domains.txt > domains-filtered.txt

cd ..

cat tmp.generated/domains-filtered.txt | sort | uniq | gzip -9 > results-gen/generated.txt.gz

rm -rf tmp.generated

