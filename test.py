import base64
from datetime import datetime

import sys

from ripe.atlas.sagan import DnsResult

from helpers import findAsn, on_result_response
from ripe.atlas.cousteau import (
    Ping,
    Dns,
    AtlasSource,
    AtlasCreateRequest,
    AtlasStream, AtlasResultsRequest)
import dns.message
import constants

dns = Dns(query_class='IN', query_type='TXT', query_argument=constants.QUERY,
          description='Pepe', af='4', protocol='UDP', is_oneoff=True, resolve_on_probe=False, target='208.67.222.222',
          include_qbuf=True, set_rd_bit=True,prepend_probe_id=True)

values = None
with open('ids.txt') as f:
    values = f.read().splitlines()

source = AtlasSource(type="probes", value=','.join(values), requested=len(values))
#source = AtlasSource(type="area", value='WW', requested=10000)

ATLAS_API_KEY = "bcbc59fb-c370-4999-bc1c-fa9fe0a9d3a9"

atlas_request = AtlasCreateRequest(
    start_time=datetime.utcnow(),
    key=ATLAS_API_KEY,
    measurements=[dns, ],
    sources=[source],
    is_oneoff=True
)
msm_id = None
create = True
if create:
    (is_success, response) = atlas_request.create()
    print response
    msm_id = response['measurements'].pop()
else:
    msm_id = 8310485

if create:
    atlas_stream = AtlasStream()
    atlas_stream.connect()
    # Measurement results
    stream_type = "result"
    # Bind function we want to run with every result message received
    atlas_stream.bind_stream(stream_type, on_result_response)
    # Subscribe to new stream for 1001 measurement results
    stream_parameters = {"msm": msm_id}
    atlas_stream.start_stream(stream_type=stream_type, **stream_parameters)
    atlas_stream.timeout(seconds=300*10)
    print "timeout"
else:
    kwargs = {
        "msm_id": msm_id,
    }
    is_success, results = AtlasResultsRequest(**kwargs).create()

    a = DnsResult(results.pop())
    b = a.responses
    for n in b:
        # print dns.message.from_wire(base64.b64decode(n.abuf))
        on_result_response(n.abuf.answers.pop())

# TODO: check that the response is the one expected
