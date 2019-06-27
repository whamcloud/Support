#!/usr/bin/python
#
# Copyright (c) 2019 DDN. All rights reserved.
#
# Run this on an agent and it will print out what needs to be in /etc/multipath/bindings
#


import os
from chroma_agent import config
from pyudev import Context

targets = config.get_section("targets")
context = Context()

for k in targets:
    target = os.path.basename(targets[k]["mntpt"])

    if not targets[k]["bdev"].startswith("/dev/mapper/"):
        continue

    mpath = os.path.basename(targets[k]["bdev"])

    device = next(
        x
        for x in context.list_devices().match_property("ID_FS_LABEL", target)
        if int(x["MAJOR"]) > 234
    )

    print("%s %s" % (mpath, device["DM_UUID"].lstrip("mpath-")))
