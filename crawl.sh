
# .se domains
wget -O - "https://www.iis.se/data/bardate_domains.txt" | cut -f 1 > se.txt

# Expired domain
sites=(deleted-com-domains deleted-net-domains deleted-org-domains deleted-de-domains deleted-info-domains deleted-biz-domains deleted-se-domains deleted-me-domains deleted-uk-domains deleted-it-domains deleted-fr-domains namecom-expired-domains godaddy-expired-domains godaddy-closeout-domains godaddy-tdnam-domains)

echo "" > expired.txt
for s in $sites
do
	for i in `seq 0 25 10000`
	do
		wget -O - "http://www.expireddomains.net/$s/?start=$i" | ./regexp.py 'title="([a-zA-Z0-9\-]+\.[a-zA-Z]+)' | tr '[:upper:]' '[:lower:]' >> expired.txt
	done
done
for u in `seq 1 7`
do
	for i in `seq 0 25 10000`
	do
		wget -O - "http://www.expireddomains.net/backorder-expired-domains/?start=$i&ftlds[]=$u" | ./regexp.py 'title="([a-zA-Z0-9\-]+\.[a-zA-Z]+)' | tr '[:upper:]' '[:lower:]' >> expired.txt
	done
done

# Moonsy
echo "" > moonsy.txt
wget -O /dev/null --save-cookies cookies.txt -U "Mozilla/5.0 (X11; Linux i686; rv:34.0) Gecko/20100101 Firefox/34.0" --referer="http://moonsy.com/expired_domains/page-1" "http://moonsy.com/expired_domains/page-1" 

for i in `seq 1 600`
do
	wget -O - --load-cookies cookies.txt -U "Mozilla/5.0 (X11; Linux i686; rv:34.0) Gecko/20100101 Firefox/34.0" --referer="http://moonsy.com/expired_domains/page-1"  "http://moonsy.com/expired_domains/page-$i" | ./regexp.py 'ydr\(.([a-zA-Z0-9\-]+\.[a-zA-Z]+).\)' >> moonsy.txt 
done


# All domains:
cat se.txt expired.txt moonsy.txt | sort | uniq > all.txt

