# Fix Volumes script

Sometimes volumes can get out of sync. This script allows you to create a mapping of targets and will then update the 
managed targets, their mounts, and volume nodes, according to the host mapping. This should then update the database such
that the volumes are mapped properly.

```python
#! /usr/bin/python

# Copyright (c) 2017 Intel Corporation. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys, os
import string

sys.path.append('/usr/share/chroma-manager')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

from chroma_core.models import ManagedHost
from chroma_core.models import Volume
from chroma_core.models import VolumeNode
from chroma_core.models import ManagedTargetMount
from chroma_core.models import ManagedTarget

# The target list should list out the OST names, the host they are associated with and their path. 
# The full list should be provided.
target_list = [
	{"name": "scratch-OST0000", "data": {"host": "oss00", "path": "/dev/mapper/mpatha"}},
	{"name": "scratch-OST0001", "data": {"host": "oss01", "path": "/dev/mapper/mpathb"}},
]

def updateTarget (managedTarget, targetEntry, targetHost, targetMount):
	print "getting volume %s" % managedTarget.volume_id
	try:
		volume = Volume.objects.get(id=managedTarget.volume_id)
	except Exception as e:
		print "Couldn't find volume id %s. This is probably because it is marked as deleted." % managedTarget.volume_id
		volume = Volume.objects.get_query_set_with_deleted().get(id=managedTarget.volume_id)
		volume.not_deleted = True
		volume.save()

	path = targetEntry['data']['path']

	volume_node = VolumeNode.objects.get(path=path, host_id=targetHost.id)
	print "Updating the VolumeNode %s to have volume %s" % (volume_node.id, volume.id)
	volume_node.volume_id = volume.id
	volume_node.save()
	print "volume node: %s volume_id: %s path: %s primary: %s" % (volume_node.id, volume_node.volume_id, volume_node.path, volume_node.primary)

	print "Updating managed target mount %s to have volume_node_id of %s." % (targetMount.id, volume_node.id)
	targetMount.volume_node_id=volume_node.id
	targetMount.save()


def update_target_entry(target_entry):	
	print "-------------------------"
	print "Updating entry %s" % target_entry
	target = target_entry['name']
	managedTarget = ManagedTarget.objects.get(name=target)
	print "managed target id: %s volume_id: %s" % (managedTarget.id, managedTarget.volume_id)
	host = ManagedHost.objects.get(fqdn=target_entry['data']['host'])
	print "managed host id: %s" % host.id
	targetMount = ManagedTargetMount.objects.get(target_id=managedTarget.id, host_id=host.id)
	print "target mount id: %s" % targetMount.id

	updateTarget(managedTarget, target_entry, host, targetMount)


def clean_volumes(volume):
	volume_nodes = len(VolumeNode.objects.filter(volume_id=volume.id))
	if volume_nodes == 0:
		print "Setting volume %s to a deleted state since there are no entries in the volume nodes table." % volume.id
		volume.not_deleted = False
		volume.save()

map(update_target_entry, target_list)
map(clean_volumes, Volume.objects.all())
```