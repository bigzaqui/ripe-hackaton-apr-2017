#!/usr/bin/env python

from infi.clickhouse_orm import models, fields, engines
from infi.clickhouse_orm.database import Database

class AtlasResults(models.Model):
    id = fields.UInt32Field()
    answer_type = fields.UInt8Field()
    rt = fields.UInt32Field()
    size = fields.UInt32Field()
    answer_rr_ttl = fields.UInt32Field()
    answer_rr_content = fields.StringField()
    prb_id = fields.UInt32Field()
    answer_rr_name = fields.StringField()
    fw = fields.UInt32Field()
    sub_id = fields.UInt32Field()
    dst_address = fields.StringField()
    sub_max = fields.UInt32Field()
    proto = fields.StringField()
    arcount = fields.UInt32Field()
    msm_name = fields.StringField()
    m_type = fields.StringField()
    msm_id = fields.UInt32Field()
    from_address = fields.StringField()
    nscount = fields.UInt32Field()
    qbuf = fields.StringField()
    abuf = fields.StringField()
    qd_count = fields.UInt32Field()
    timestamp = fields.DateTimeField()
    lts = fields.UInt32Field()
    af = fields.UInt32Field()
    an_count = fields.UInt32Field()
    src_addr = fields.StringField()
    date = fields.DateField()

    engine = engines.MergeTree('date', ('id', 'date'))

class CensorshipResults(models.Model):
    hostname = fields.StringField()
    domain = fields.StringField()
    client_ip = fields.StringField()
    ns_ip = fields.StringField()
    censored = fields.UInt8Field()
    date = fields.DateField()

    engine = engines.MergeTree('date', ('domain', 'hostname'))