# Copyright (c) 2019 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

#! /usr/bin/python

import sys, os
import string
from functools import partial

sys.path.append("/usr/share/chroma-manager")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from django.conf import settings

from chroma_core.models import VolumeNode
from chroma_core.models import ManagedTarget
from chroma_core.models import ManagedTargetMount

# Get all target mounts
target_mounts = ManagedTargetMount.objects.all()
volume_nodes = VolumeNode.objects.all()

def has_deleted_volume_node(target_mount):
    node = target_mount.volume_node
    return node.not_deleted is None

def get_volume_node_by_path_and_host(path, host_id, volume_node):
  return volume_node.path == path and volume_node.host.id is host_id and volume_node.not_deleted

def get_inactive_managed_targets(target):
  return target.active_mount_id is None

# determine which target mounts are assigned a deleted volume node
dirty_target_mounts = filter(has_deleted_volume_node, target_mounts)

for target_mount in dirty_target_mounts:
  matching_volume_node = filter(partial(get_volume_node_by_path_and_host, target_mount.volume_node.path, target_mount.host.id), volume_nodes)
  print "Setting target mount {} to have a volume id of {}".format(target_mount.id, matching_volume_node[0].id)
  target_mount.volume_node_id = matching_volume_node[0].id
  print "Setting target {} to have a volume id of {}".format(target_mount.target.id, matching_volume_node[0].volume_id)
  target_mount.target.volume_id = matching_volume_node[0].volume_id
  print "Saving target mount data"
  target_mount.save()

targets = ManagedTarget.objects.all()
target_mounts = ManagedTargetMount.objects.all()

# Determine which target mounts are inactive
inactive_targets = filter(get_inactive_managed_targets, targets)

# Locate the appropriate target mount for targets that don't have one assigned
for target in inactive_targets:
  matching_mounts = filter(lambda x: x.target_id is target.id, target_mounts)
  primary = filter(lambda x: x.primary, matching_mounts)[0]
  print "setting inactive target {} to target mount id {}".format(target.id, primary.id)
  target.active_mount_id = primary.id
  target.save()

print "Targets have now been updated."