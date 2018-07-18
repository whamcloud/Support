# Copyright (c) 2018 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys
import os
import json

sys.path.append('/usr/share/chroma-manager')  # noqa: E402
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'   # noqa: E402
from django.core import serializers
from chroma_core.lib.util import CommandLine


cl = CommandLine()
try_shell = cl.try_shell


def cont():
    cont = raw_input("    Continue? (y/n)").lower()
    if cont not in ['y', 'yes']:
        sys.exit(1)


def try_remote_command(fqdn, cmd):
    rc, out, err = try_shell(['ssh', "root@%s" % fqdn, cmd])
    print "    rc: %s stdout: %s stderr: %s" % (rc, out, err)


def printQuery(q):
    q_json = serializers.serialize('json', q)
    parsed = json.loads(q_json)
    print json.dumps(parsed, indent=2, sort_keys=True)
