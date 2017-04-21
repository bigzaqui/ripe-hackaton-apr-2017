import requests
import constants

def findAsn(ip):
    try:
        r = requests.get("https://stat.ripe.net/data/network-info/data.json?resource=%s" % ip)
        result = r.json()
        if result:
            return result['data']['asns'][0]
        else:
            return False
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
                        if findAsn(ip) != '15169':
                            allgoogle = False
                            break
                exittext += "google!" if allgoogle else ":("
                exittext += ", {} ocurrences in the logs".format(counter)
                print exittext
        else:
            print "{}, no answer".format(args[0]['prb_id'])
    except:
        print args[0]