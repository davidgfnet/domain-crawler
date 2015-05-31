#!/bin/bash

mkdir -p results/
mkdir tmp.es/
cd    tmp.es/

wget -l 1  --no-directories -A pdf -r  "http://www.dominios.es/dominios/es/todo-lo-que-necesitas-saber/estadisticas"
echo "" > all.txt

for file in *
do
	pdftotext "$file" "$file.txt"
	rm "$file"
	if [ -f "$file.txt" ]; then
		../parser.py "es,com.es,org.es,nom.es,gob.es,edu.es" "$file.txt" >> all.txt
	fi
done

sort all.txt > all.sorted.txt
cat all.sorted.txt | uniq | gzip -9 > ../results/dot.es.txt.gz

cd ..
rm -rf tmp.es

