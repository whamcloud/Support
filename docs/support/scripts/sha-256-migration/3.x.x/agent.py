# Copyright (c) 2018 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import time

from chroma_core.lib.util import CommandLine
cl = CommandLine()
try_shell = cl.try_shell


def upload_file(h, file):
    try:
        target = "{0}:{1}".format(h, file)
        print "    - Uploading {0} to {1}".format(file, target)
        try_shell(['scp', file, target])
    except Exception as e:
        print "Could not copy {0}.".format(file)
        print e


def generate_private_key(h):
    try:
        print "    - Generating private key on {0}".format(h)
        try_shell(['ssh',
                   "root@{0}".format(h),
                   'openssl genrsa -out /var/lib/chroma/private.pem \
2048 -sha256'])
    except Exception as e:
        print "Could not generate private key on {0}".format(h)
        print e


def backup_certificates(h):
    try:
        print "    - Backing up certificates on {0}".format(h)
        ts = int(time.time())
        target_dir = "/var/lib/chroma/backup_{0}".format(ts)
        try_shell(['ssh',
                   "root@{0}".format(h),
                   "mkdir {0} && cp /var/lib/chroma/*.crt {1}\
".format(target_dir, target_dir)])
    except Exception as e:
        print "Could not backup certificates on {0}".format(h)
        print e


def create_self_certificate(h, serial):
    try:
        print "    - Creating new certificate on {0}".format(h)
        rc, cert_request, err = try_shell([
            'ssh',
            "root@{0}".format(h),
            "openssl req -new -sha256 -subj /C=/ST=/L=/O=/CN={0} \
-key /var/lib/chroma/private.pem".format(h)])

        rc, new_cert, err = try_shell([
            'openssl',
            'x509',
            '-req',
            '-sha256',
            '-days',
            '36500',
            '-CAkey',
            '/var/lib/chroma/authority.pem',
            '-CA',
            '/var/lib/chroma/authority.crt',
            '-set_serial',
            "0x{0}".format(serial)],
            stdin_text=cert_request)
        try_shell(['ssh',
                   "root@{0}".format(h),
                   'cat > /var/lib/chroma/self.crt'],
                  stdin_text=new_cert)
    except Exception as e:
        print "Could not create certificate file on {0}".format(h)
        print e


def restart(h):
    try:
        print "    - Restarting Agent on {0}".format(h)
        rc, out, err = try_shell(['ssh',
                                  "root@{0}".format(h),
                                  'service chroma-agent restart'])
    except Exception as e:
        print "Could not restart agent on {0}".format(h)
        print e
