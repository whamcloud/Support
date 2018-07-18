# Copyright (c) 2018 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys
import time
import glob

sys.path.append('/usr/share/chroma-manager')

from django.core.management import setup_environ
import settings
setup_environ(settings)

from chroma_core.lib.util import CommandLine
cl = CommandLine()
try_shell = cl.try_shell

from chroma_core.lib.service_config import ServiceConfig


def backup_certs_and_pems():
    try:
        ts = int(time.time())
        target_dir = "/var/lib/chroma/backup_{0}".format(ts)
        try_shell(['mkdir', target_dir])
        certs = glob.glob('/var/lib/chroma/*.crt')
        print "    - Backing up certificates and pem files to \
{0}".format(target_dir)
        try_shell(['cp'] + certs + [target_dir])
        pems = glob.glob('/var/lib/chroma/*.pem')
        try_shell(['cp'] + pems + [target_dir])
    except Exception as e:
        print 'Could not backup certificates in /var/lib/chroma'
        print e


def update_manager_file(remove_path, from_path, to_path):
    try:
        print '    - Updating {0} on manager node.'.format(to_path)
        try_shell([
            'rm',
            '-f',
            remove_path
        ])

        try_shell([
            'cp',
            from_path,
            to_path
        ])
    except Exception as e:
        print 'Could not replace {0} on the manager.'.format(to_path)
        print e


def update_manager_crypto():
    return update_manager_file(
        '/usr/share/chroma-manager/chroma_core/services/http_agent/crypto.pyc',
        'chroma_manager_crypto.py',
        '/usr/share/chroma-manager/chroma_core/services/http_agent/crypto.py'
    )


def update_view():
    return update_manager_file(
        '/usr/share/chroma-manager/chroma_agent_comms/views.pyc',
        'views.py',
        '/usr/share/chroma-manager/chroma_agent_comms/views.py'
    )


def restart():
    print '\nRestarting Manager:'
    service_config = ServiceConfig()
    service_config.stop()
    service_config.start()
