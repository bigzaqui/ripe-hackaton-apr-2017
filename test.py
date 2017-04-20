import base64
from datetime import datetime
from ripe.atlas.cousteau import (
    Ping,
    Dns,
    AtlasSource,
    AtlasCreateRequest,
    AtlasStream, AtlasResultsRequest)
import dns.message

dns = Dns(query_class='IN', query_type='TXT', query_argument='google.com',
          description='Pepe', af='4', protocol='UDP', is_oneoff=True, target='8.8.8.8')

dns = Dns(query_class='IN', query_type='A', query_argument='google.com',
          description='Pepe', af='4', protocol='UDP', is_oneoff=True, target='8.8.8.8')

source = AtlasSource(type="area", value="WW", requested=1)

ATLAS_API_KEY = "bcbc59fb-c370-4999-bc1c-fa9fe0a9d3a9"

atlas_request = AtlasCreateRequest(
    start_time=datetime.utcnow(),
    key=ATLAS_API_KEY,
    measurements=[dns, ],
    sources=[source],
    is_oneoff=True
)

#(is_success, response) = atlas_request.create()
#print response

kwargs = {
    "msm_id": 8310265,
}

is_success, results = AtlasResultsRequest(**kwargs).create()

for r in results:
    print r

from ripe.atlas.sagan import DnsResult
from ripe.atlas.sagan.dns import Response, Message
import base64
import dns.message
a = DnsResult(r)
b = a.responses
for n in b:
    #print dns.message.from_wire(base64.b64decode(n.abuf))
    print n.abuf.answers
