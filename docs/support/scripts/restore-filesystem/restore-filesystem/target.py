# Copyright (c) 2018 Intel Corporation. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys
import os
import shell

sys.path.append('/usr/share/chroma-manager')  # noqa: E402
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'   # noqa: E402
from chroma_core.models import ManagedTarget, ManagedTargetMount, ManagedMdt
from chroma_core.models import VolumeNode, Volume, ManagedHost, ManagedOst
from chroma_core.models import ManagedMgs


def getFsOSTs(filesystemId):
    return map(
        lambda ost: ManagedTarget.objects.get_query_set_with_deleted().get(
            id=ost.managedtarget_ptr_id),
        ManagedOst.objects.get_query_set_with_deleted().filter(
            filesystem_id=filesystemId
        )
    )


def getFsMDTs(filesystemId):
    return map(
        lambda mdt: ManagedTarget.objects.get_query_set_with_deleted().get(
            id=mdt.managedtarget_ptr_id),
        ManagedMdt.objects.get_query_set_with_deleted().filter(
            filesystem_id=filesystemId
        )
    )


def getFsMGS():
    return ManagedTarget.objects.get(
      id=ManagedMgs.objects.all()[0].managedtarget_ptr_id
    )


def getActiveMount(target):
    try:
        mount = ManagedTargetMount.objects.get_query_set_with_deleted().get(
            target_id=target.id, primary=True)
        return mount
    except Exception as e:
        print "    Couldn't retrieve target mount for \
%s: %s" % (target.name, e)
        shell.cont()


def activateTarget(target, state):
    target.state = state
    target.not_deleted = True
    mount = getActiveMount(target)
    if mount:
        target.active_mount_id = mount.id

    target.save()


def activateMDTs(mdts):
    for mdt in mdts:
        activate = raw_input(
          "    Activate MDT '%s' with a state of 'unmounted'? (y/n)" % mdt.name
        ).lower()

        if activate in ['y', 'yes']:
            activateTarget(mdt, 'unmounted')
            print "    New MDTs:"
            shell.printQuery(mdts)


def activateOSTs(osts):
    for ost in osts:
        activate = raw_input(
          "    Activate OST '%s' with a state of unmounted? (y/n)" % ost.name
        ).lower()
        if activate in ['y', 'yes']:
            activateTarget(ost, 'unmounted')
            print "    New OSTs:"
            shell.printQuery(osts)


def activateMGS(mgs):
    activate = raw_input(
      "    Activate MGS '%s' with a state of mounted? (y/n)" % mgs.name
    ).lower()
    if activate in ['y', 'yes']:
        activateTarget(mgs, 'mounted')
        print "    New MGS: id: %d, name: %s, state: %s, uuid: %s, ha_label: \
%s" % (
          mgs.id,
          mgs.name,
          mgs.state,
          mgs.uuid,
          mgs.ha_label
        )


def getTargets():
    return ManagedTarget.objects.all()


def registerTarget(target, volume_node, mount, volume, host):
    register = raw_input(
      "    Register target %s with path %s mounted on %s using type %s on host %s? \
(y/n)" % (
        target.name,
        volume_node.path,
        mount.mount_point,
        volume.filesystem_type,
        host.fqdn
      )
    ).lower()

    if register in ['y', 'yes']:
        try:
            print "    Registering target %s on %s." % (target.name, host.fqdn)
            cmd = "chroma-agent register_target --target_name %s \
--device_path %s --mount_point %s --backfstype %s" % (
                    target.name,
                    volume_node.path,
                    mount.mount_point,
                    volume.filesystem_type
                )
            shell.try_remote_command(host.fqdn, cmd)
        except Exception as e:
            print "    Couldn't register target %s on %s: %s" % (
                target.name, host.fqdn, e)
            shell.cont()


def configureTargetStore(target, volume_node, mount, volume, host):
    configure = raw_input(
      "    Configure target %s with path %s mounted on %s using type %s on \
host %s? (y/n)" % (
        target.name,
        volume_node.path,
        mount.mount_point,
        volume.filesystem_type,
        host.fqdn
      )
    ).lower()

    if configure in ['y', 'yes']:
        try:
            print "    Configuring target %s on %s." % (target.name, host.fqdn)
            cmd = "chroma-agent configure_target_store --device %s --uuid %s \
--mount_point %s --backfstype %s --target_name %s" % (
                    volume_node.path,
                    target.uuid,
                    mount.mount_point,
                    volume.filesystem_type,
                    target.name
                )
            shell.try_remote_command(host.fqdn, cmd)
        except Exception as e:
            print "    Couldn't configure target store for target \
%s on %s: %s" % (
                target.name,
                host.fqdn,
                e
            )
            shell.cont()


def updateTarget(target):
    update = raw_input("    Update target %s? (y/n)" % target.name).lower()

    if update in ['y', 'yes']:
        volume_node = VolumeNode.objects.get_query_set_with_deleted().get(
            volume_id=target.volume_id, primary=True)
        mount = ManagedTargetMount.objects.get_query_set_with_deleted().get(
            volume_node_id=volume_node.id)
        volume = Volume.objects.get_query_set_with_deleted().get(
            id=target.volume_id
        )
        host = ManagedHost.objects.get_query_set_with_deleted().get(
            id=mount.host_id
        )

        registerTarget(target, volume_node, mount, volume, host)
        configureTargetStore(target, volume_node, mount, volume, host)


def startTarget(target):
    volume_node = VolumeNode.objects.get_query_set_with_deleted().get(
        volume_id=target.volume_id, primary=True)
    mount = ManagedTargetMount.objects.get_query_set_with_deleted().get(
        volume_node_id=volume_node.id)
    host = ManagedHost.objects.get_query_set_with_deleted().get(
        id=mount.host_id
    )

    start = raw_input(
      "    Start target %s with path %s mounted on %s on host %s? (y/n)" % (
        target.name,
        volume_node.path,
        mount.mount_point,
        host.fqdn
      )
    ).lower()

    if start in ['y', 'yes']:
        try:
            print "    Starting target %s on %s." % (target.name, host.fqdn)
            cmd = "chroma-agent start_target --ha_label %s" % (target.ha_label)
            shell.try_remote_command(host.fqdn, cmd)
        except Exception as e:
            print "    Couldn't start target %s on %s: %s" % (
                target.name, host.fqdn, e)
            shell.cont()
