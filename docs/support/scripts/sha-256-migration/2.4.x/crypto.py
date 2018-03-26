# Copyright (c) 2018 Intel Corporation. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import os
import re
import settings

from chroma_core.lib.util import CommandLine
cl = CommandLine()
try_shell = cl.try_shell

from functools import partial

crypto_folder = partial(os.path.join, settings.CRYPTO_FOLDER)
AUTHORITY_KEY_FILE = crypto_folder('authority.pem')
AUTHORITY_CERT_FILE = crypto_folder('authority.crt')
MANAGER_KEY_FILE = crypto_folder('manager.pem')
MANAGER_CERT_FILE = crypto_folder('manager.crt')
CERTIFICATE_DAYS = "36500"

def create_private_key(filename):
    try_shell(['openssl', 'genrsa', '-out', filename, '2048', '-sha256'])
    print '    - Generated Private Key: %s' % filename

def create_authority_key_and_cert():
    def create_authority_key():
        create_private_key(AUTHORITY_KEY_FILE)

    def create_authority_cert():
        rc, csr, err = try_shell(["openssl", "req", "-new", "-sha256", "-subj", "/C=/ST=/L=/O=/CN=x_local_authority", "-key", AUTHORITY_KEY_FILE])
        rc, out, err = try_shell(["openssl", "x509", "-req", "-sha256", "-days", CERTIFICATE_DAYS, "-signkey", AUTHORITY_KEY_FILE, "-out", AUTHORITY_CERT_FILE], stdin_text = csr)
        print '    - Created Authority Certificate using sha256: %s' % AUTHORITY_CERT_FILE

    create_authority_key()
    create_authority_cert()


def create_manager_key_and_cert(name):
    def create_manager_key():
        return create_private_key(MANAGER_KEY_FILE)

    def create_manager_cert(name):
        rc, csr, err = try_shell(["openssl", "req", "-new", "-sha256", "-subj", "/C=/ST=/L=/O=/CN=%s" % name, "-key", MANAGER_KEY_FILE])
        rc, out, err = try_shell(["openssl", "x509", "-req", "-sha256", "-days", CERTIFICATE_DAYS, "-CA", AUTHORITY_CERT_FILE, "-CAcreateserial", "-CAkey", AUTHORITY_KEY_FILE, "-out", MANAGER_CERT_FILE], stdin_text = csr)
        print "    - Created Manager Certificate using sha256: %s" % MANAGER_CERT_FILE

    create_manager_key()
    create_manager_cert(name)
