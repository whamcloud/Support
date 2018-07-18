#! /usr/bin/python

# Copyright (c) 2018 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys
import os
import string
import time
import json
from functools import partial
import shell
import filesystem
import target
import ha
import manager

sys.path.append('/usr/share/chroma-manager')  # noqa: E402
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'   # noqa: E402
from chroma_core.models import ManagedFilesystem, ManagedTarget
from chroma_core.models import ManagedTargetMount, ManagedOst, ManagedMdt
from chroma_core.models import ManagedHost, Volume, VolumeNode
from chroma_core.lib.util import CommandLine

cl = CommandLine()
try_shell = cl.try_shell

print "--- Filesystem ---"
selected_filesystem = filesystem.getFilesystem()
print "    ------------------------------------------------------------"
print "    Current Filesystem state: id: %s, name: %s, state: %s" % (
    selected_filesystem.id,
    selected_filesystem.name,
    selected_filesystem.state
)
filesystem.setFilesystemToAvailableState(selected_filesystem)

mgs = target.getFsMGS()
print "--- MGS ---"
print "    Current MGS: id: %d, name: %s, state: %s, uuid: %s, \
ha_label: %s" % (
    mgs.id,
    mgs.name,
    mgs.state,
    mgs.uuid,
    mgs.ha_label
)
print "    *Note* - If your MGS is already mounted there is no need \
to activate."
target.activateMGS(mgs)

mdts = target.getFsMDTs(selected_filesystem.id)
print "--- MDTs ---"
print "    Current MDTs:"
shell.printQuery(mdts)
target.activateMDTs(mdts)

osts = target.getFsOSTs(selected_filesystem.id)
print "--- OSTs ---"
print "    Current OSTs:"
shell.printQuery(osts)
target.activateOSTs(osts)

hosts = ManagedHost.objects.all()
print "--- Hosts ---"
shell.printQuery(hosts)
print "------------------------------------------------------------"

for host in hosts:
    ha.stopAgent(host)
    ha.turnOnMaintenanceMode(host)

print "--- High Availability ---"
update_pacemaker = raw_input("    Update pacemaker configs? (y/n)").lower()
if update_pacemaker in ['y', 'yes']:
    new_cib_location = '/tmp/selected_cib.xml'
    for host in hosts:
        ha.updatePacemaker(host, new_cib_location)
        ha.stopPacemaker(host)
        ha.stopCorosync(host)
        ha.startCorosync(host)
        ha.startPacemaker(host)
        ha.turnOnMaintenanceMode(host)

print "--- Preparing Targets ---"
print "    *Note* - If your MGS is already configured there \
is no need to do it again."

targets = target.getTargets()
for cur_target in targets:
    target.updateTarget(cur_target)

print "--- Manager ---"
manager.restartManager()

for host in hosts:
    ha.turnOffMaintenanceMode(host)
    ha.startAgent(host)

print "Filesystem '%s' is now configured. You may need to wait \
10 to 20 minutes before attempting to start \
the targets." % selected_filesystem.name

print "Process completed."
