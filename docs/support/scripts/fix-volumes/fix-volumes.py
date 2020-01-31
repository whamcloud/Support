#! /usr/bin/env python

import sys
import os
​
sys.path.append('/usr/share/chroma-manager')
​
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
​
from django.db import connection
​
​
def update_mtms(cursor):
	cursor.execute("select mtm.id, vn.volume_id, vn.id from chroma_core_managedtargetmount mtm left join chroma_core_volumenode vn on mtm.volume_node_id = vn.id where mtm.not_deleted = 't' and vn.not_deleted is Null")
​
	rows = cursor.fetchall()
​
	if len(rows) == 0:
		print("No target mounts need updating")
		return
​
	(out_of_date_target_mounts, out_of_date_volumes, out_of_date_volumenodes) = zip(*rows)
​
	cursor.execute("select label, id from chroma_core_volume where id in %s", [out_of_date_volumes])
​
	(old_labels, old_volume_ids) = zip(*cursor.fetchall())
​
	cursor.execute("select label, id from chroma_core_volume where label in %s and not_deleted = 't'", [old_labels])
	(new_labels, new_volumes) = zip(*cursor.fetchall())
​
	cursor.execute("select id, volume_id from chroma_core_volumenode where volume_id in %s and not_deleted = 't'", [new_volumes])
	(new_volume_nodes, new_volumes2) = zip(*cursor.fetchall())
​
	for idx, volume in enumerate(new_volumes2):
		new_volume_idx = new_volumes.index(volume)
		new_label = new_labels[new_volume_idx]
​
		old_label_idx = old_labels.index(new_label)
		old_volume_id = old_volume_ids[old_label_idx]
​
		old_volume_idx = out_of_date_volumes.index(old_volume_id)
​
		old_target_mount = out_of_date_target_mounts[old_volume_idx]
		old_volume_node = out_of_date_volumenodes[old_volume_idx]
		new_volume_node = new_volume_nodes[idx]
​
		print("updating target mount: {} from volume node: {},  to volume node {}".format(old_target_mount, old_volume_node, new_volume_node))
​
		cursor.execute("UPDATE chroma_core_managedtargetmount SET volume_node_id = %s WHERE id = %s", [new_volume_node, old_target_mount])
​
​
def update_targets(cursor):
	cursor.execute("select mt.id, v.label from chroma_core_managedtarget mt left join chroma_core_volume v on mt.volume_id = v.id where mt.not_deleted = 't' and v.not_deleted is Null")
	rows = cursor.fetchall()
​
	if len(rows) == 0:
		print("No targets need updating")
		return
​
	(out_of_date_targets, out_of_date_labels) = zip(*rows)
​
	
	cursor.execute("select id, label from chroma_core_volume where label in %s and not_deleted = 't'", [out_of_date_labels])
	(new_volumes, new_labels) = zip(*cursor.fetchall())
​
	
​
	if len(out_of_date_targets) != len(new_volumes):
		eprint("New volumes do not match targets")
		exit(1)
​
	for idx, volume_id in enumerate(new_volumes):
		new_label = new_labels[idx]
		old_label_idx = out_of_date_labels.index(new_label)
		target_id = out_of_date_targets[old_label_idx]
​
		print("updating target: {} to volume id: {}".format(target_id, volume_id))
​
		cursor.execute("UPDATE chroma_core_managedtarget SET volume_id = %s WHERE id = %s", [volume_id, target_id])
​
​
try:
	cursor = connection.cursor()
​
	update_targets(cursor)
	update_mtms(cursor)
​
finally:
	cursor.close()