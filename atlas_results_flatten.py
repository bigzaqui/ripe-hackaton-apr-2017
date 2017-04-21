#!/usr/bin/env python3

# Sorry for my ugliesh python3

from datetime import datetime
from ripe.atlas.cousteau import AtlasResultsRequest
import base64
import dns.message
import copy
import json

kwargs = {
    "msm_id": 8309609,
    # "start": datetime(2015, 5, 19),
    # "stop": datetime(2015, 5, 20),
    # "probe_ids": [1,2,3,4]
}

# results = json.load(open('./results.json'))

is_success, results = AtlasResultsRequest(**kwargs).create()

if not is_success:
    exit()

flatlist = []
errors = {"count": 0, "error_list": [] }

rows = []

def dict_splitter():
    return


# We need it to put data into clickhouse
# It little bit ugly
def make_flatten(input_dict):
    return_list = []
    count = 0
    top_elements = {}
    elements_to_expand = []
    for n, field in enumerate(input_dict):
        if isinstance(input_dict[field], list):
            count += 1
            elements_to_expand.append(field)
        else:
            top_elements[field] = result_m[field]

    expanded_list = [copy.deepcopy(item) for item in input_dict['resultset']]
    for i in expanded_list:
        i.update(top_elements)

    for i in expanded_list:
        if 'error' in i:
            # print("ERROR! {}".format(i['error']))
            # errors['count'] += 1
            # errors['error_list'].append(result)
            error = {}
            for e_name, e_value in i['error'].items():
                error['error_{}'.format(e_name)] = e_value
            i.update(error)
            # del (i['error'])
            continue
        i.update(i['result'])
        del(i['result'])

    full_expanded_list = []
    for i in expanded_list:
        if 'error' in i:
            del(i['error'])
            full_expanded_list.append(i)
            continue
        dnsmsg = dns.message.from_wire(
            base64.b64decode(i['abuf']))
        for x in dnsmsg.answer:
            for y in x.items:
                rr_data = {'answer_rr_name': str(x.name),
                           'answer_rr_ttl': int(x.ttl),
                           'answer_rr_content': y.address,
                           'answer_rr_type': y.rdtype}
                # print("{} {} {}".format(x.name, x.ttl, y))
                # print("{}".format(rr_data))
                rr_data.update(i)
                full_expanded_list.append(rr_data)

    # print(top_elements)
    # print(json.dumps(full_expanded_list, indent=2))
    return(full_expanded_list)

all_fields = {}

for result_m in results:
    print("Probe {} from: {}".format(result_m['prb_id'],result_m["from"]))

    top_elements = {}

    d = make_flatten(result_m)

    for i in d:
        print(json.dumps(i, indent=2))
        for num, field_name in enumerate(i):
            if field_name in all_fields:
                all_fields[field_name] += 1
            else:
                all_fields[field_name] = 0
    # for result in result_m["resultset"]:
    #     top_result_element = copy.copy(top_elements)
    #     if 'error' in result:
    #         print("ERROR! {}".format(result['error']))
    #         errors['count'] += 1
    #         errors['error_list'].append(result)
    #         continue
    #     dnsmsg = dns.message.from_wire(
    #         base64.b64decode(result['result']['abuf']))
    #     for i in dnsmsg.answer:
    #         # print(i)
    #         for y in i.items:
    #             print(y)


print(json.dumps(all_fields, indent=2))
# print("Errors: {}".format(errors))
    # print(result)