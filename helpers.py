#!/usr/bin/env python

import requests
import constants
import init_db
from init_db import CensorshipResults
import datetime
from geoip import geolite2

from infi.clickhouse_orm.database import Database

def findAsn(ip):
    try:
        r = requests.get("https://stat.ripe.net/data/network-info/data.json?resource=%s" % ip)
        result = r.json()
        return result['data']['asns'][0]
    except:
        # failed to lookup as-number
        return False

def on_result_response(*args):
    """
    Function that will be called every time we receive a new result.
    Args is a tuple, so you should use args[0] to access the real message.
    """
    db = Database('dnshackaton')
    db.create_table(CensorshipResults)

    if not db:
        print "No DB connection"
        exit(1)
    ip = None
    ans = args[0]['result']
    if 'answers' in ans:
        hostname = ans['answers'].pop()['NAME']
        exittext = "{} -> ".format(hostname)
        with open('querylog2') as f:
            allgoogle = True
            counter = 0
            for line in f:
                if hostname in line:
                    counter +=1
                    ip = line.split(' ')[6].split('#')[0]
                    if findAsn(ip) != '15169':
                        allgoogle = False
                        break
            if allgoogle and hostname:
                res = CensorshipResults(hostname=hostname,
                                        domain=line.split(' ')[7].split('#')[0].translate(None, '(:)'),
                                        client_ip=line.split(' ')[6].split('#')[0],
                                        ns_ip=line.split(' ')[13].split('#')[0].translate(None, '(:)'),
                                        censored=0, date=datetime.date.today(),ts=datetime.datetime.now())
                db.insert([res])
            else:
                res = CensorshipResults(hostname=hostname,
                                        domain=line.split(' ')[7].split('#')[0].translate(None, '(:)'),
                                        client_ip=line.split(' ')[6].split('#')[0],
                                        ns_ip=line.split(' ')[13].split('#')[0].translate(None, '(:)'),
                                        censored=1, date=datetime.date.today(),ts=datetime.datetime.now())
                db.insert([res])
            exittext += "google!" if allgoogle else ":("
            exittext += ", {} ocurrences in the logs".format(counter)
            print exittext
    else:
        print "{}, no answer".format(args[0]['prb_id'])
