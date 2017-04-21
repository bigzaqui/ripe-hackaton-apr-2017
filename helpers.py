import requests
import constants
import dns.reversename
import dns.resolver

def findAsn(ip):
    try:
        reverse = dns.reversename.from_address(ip)
        if 'in-addr' in reverse:
            lookup = str(reverse).replace('in-addr.arpa','origin.asn.cymru.com') 
        else:
            lookup = str(reverse).replace('ip6.arpa','origin6.asn.cymru.com') 
        return str(dns.resolver.query(lookup, 'TXT')[0]).split(' ')[0].replace('"','').strip()
    except: 
        # failed to lookup as-number
        return False

def findAsnName(asn):
    try:
        return str(dns.resolver.query("AS{0}.asn.cymru.com".format(asn) , 'TXT')[0]).split('|')[4].replace('"','').replace(",","").strip()
    except: 
        # failed to lookup as-number
        return False

def on_result_response(*args):
    """
    Function that will be called every time we receive a new result.
    Args is a tuple, so you should use args[0] to access the real message.
    """
    try:
        ip = None
        if 'result' not in args[0]:
            return False
        ans = args[0]['result']
        if 'answers' in ans:
            hostname = ans['answers'].pop()['NAME']
            exittext = "{} -> ".format(hostname)
            with open('/usr/local/etc/namedb/log/querylog') as f:
                allgoogle = True
                counter = 0
                for line in f:
                    if hostname in line:
                        counter +=1
                        ip = line.split(' ')[6].split('#')[0]
                        if findAsn(ip) != '36692':
                            allgoogle = False
                            break
                exittext += "google!" if allgoogle else ":("
                exittext += ", {} ocurrences in the logs".format(counter)
                print exittext
        else:
            print "{}, no answer".format(args[0]['prb_id'])
    except:
        print args[0]
