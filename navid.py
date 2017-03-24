#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import json

import snakemq
import snakemq.link
import snakemq.packeter

from navi.core import Navi
from navi.config import NaviConfig
from navi.cli import NaviCli

resp_success = {'response': 'success'}

def on_recv(conn, packet):
    try:
        msg = json.loads(packet)
        if msg['type'] == "message":
            navi.push_msg(msg['payload'])
        elif msg['type'] == "file":
            navi.push_media(str(msg['payload']))
        else:
            raise ValueError('Unknown type')
        pktr.send_packet(conn, json.dumps(resp_success))
    except Exception as e:
        resp_err = {'response': str(e)}
        pktr.send_packet(conn, json.dumps(resp_err))

s = snakemq.link.Link()
s.add_listener(("", 4000))

pktr = snakemq.packeter.Packeter(s)
pktr.on_packet_recv.add(on_recv)

args = NaviCli()
config = NaviConfig(args.config_file)
try:
    navi = Navi(config.server_host_url,
            config.client_user_id,
            config.client_user_password,
            config.notification_users,
            quiet=args.quiet)
except requests.ConnectionError:
    sys.stderr.write("Connection problem\n")
    sys.exit(-1)

s.loop()
