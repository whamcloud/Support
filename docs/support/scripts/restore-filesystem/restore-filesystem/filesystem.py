# Copyright (c) 2018 Intel Corporation. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys
import os

sys.path.append('/usr/share/chroma-manager')  # noqa: E402
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'   # noqa: E402
from chroma_core.models import ManagedFilesystem


def getFilesystem():
    filesystems = ManagedFilesystem.objects.get_query_set_with_deleted()
    print "Filesystems:"
    for filesystem in filesystems:
        print "%d: %s" % (filesystem.id, filesystem.name)
    fs_id = raw_input("    Enter the filesystem id to recover:")

    try:
        selected_filesystem = ManagedFilesystem.objects \
          .get_query_set_with_deleted().get(id=fs_id)
        print "    Selected filesystem: %s" % selected_filesystem.name
        return selected_filesystem
    except Exception as e:
        print "    Error retrieving the selected filesystem: %s" % e
        try_again = raw_input(
          "    Attempt to select filesystem again? (y/n)"
        ).lower()
        if try_again in ['y', 'yes']:
            return getFilesystem()
        else:
            sys.exit(1)


def setFilesystemToAvailableState(filesystem):
    set_available = raw_input(
      "    Set filesystem %s to available state? (y/n)" %
      filesystem.name
    ).lower()

    if set_available in ['y', 'yes']:
        try:
            filesystem.state = 'available'
            filesystem.not_deleted = True
            filesystem.save()

            print "    New Filesystem state: id: %s, name: %s, state: %s" % (
              filesystem.id,
              filesystem.name,
              filesystem.state
            )
        except Exception as e:
            print "    Error retrieving the selected filesystem: \n%s" % e
            sys.exit(1)
