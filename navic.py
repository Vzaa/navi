#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

import snakemq
import snakemq.link
import snakemq.packeter

from navi.cli import NaviCli

recv_count = 0
send_count = 0

def on_connect(conn):
    global send_count
    if args.media is not None:
        for med in args.media:
            msg = {"type": "file", "payload": med}
            send_count += 1
            pktr.send_packet(conn, json.dumps(msg))

    if args.message is not None:
        msg = {"type": "message", "payload": args.message}
        send_count += 1
        pktr.send_packet(conn, json.dumps(msg))

def on_recv(conn, packet):
    global recv_count
    resp = json.loads(packet)
    print(resp['response'])
    recv_count += 1
    if recv_count == send_count:
        sys.exit(0)

args = NaviCli()
s = snakemq.link.Link()
s.add_connector(("localhost", 4000))

pktr = snakemq.packeter.Packeter(s)
pktr.on_connect.add(on_connect)
pktr.on_packet_recv.add(on_recv)

s.loop()
