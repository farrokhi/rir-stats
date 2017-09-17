#!/bin/sh
#
# Note:
#
# 1- This script relies on pcregrep (installed separately) for multiline regexp matching
# 2- "{" is chosen as CSV field separator in order to avoid conflicting with standard characters used in description field
#
# RPSL DBs taken from:
#  ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.route.gz
#  ftp://ftp.arin.net/pub/rr/arin.db
#  ftp://ftp.radb.net/radb/dbase/*.db (e.g. savvis, radb)
#

if [ $# -lt 1 ]; then
	echo "error: please specify input file"
	exit 1
fi

if [ ! -r $1 ]; then
	echo "error: cannot open $1 for reading"
	exit 1
fi

pcregrep --om-separator='{' -o1 -o2 -M '^route:[\s]+(.+)$[\n]descr:[ ]+(.+)$' $1 | awk -F '{' '{printf "%s,^%s^\n",$1,$2}' | iconv -f ISO-8859-1 -t utf-8 | sed -E -e 's/[ ]+,/,/' -e 's/^[\s]+//g'
