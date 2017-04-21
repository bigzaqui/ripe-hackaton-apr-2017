#!/usr/bin/env python
from helpers import findAsn
from helpers import findAsnName
import sys
#simple tool to play with dns query logs reformating into simple cvs output
#filter-querylog.py "url filter" "asn to match against"
with open('/usr/local/etc/namedb/log/querylog' , 'r')  as f:
  for line in f:
    if sys.argv[1] in line:
      request_from = line.split(' ')[6].split('#')[0] 
      probe_id = line.split(' ')[7].split('.')[0].replace('(','')
      timestamp = line.split(' ')[7].split('.')[1] 
      asn = findAsn(request_from) 
      asnname = findAsnName(asn) 
      if asn == sys.argv[2]:
         result = ':)'
      else:
         result = ':('
      print "{0},{1},{2},{3},{4},{5}".format(probe_id,timestamp,request_from,asn,result,asnname)

