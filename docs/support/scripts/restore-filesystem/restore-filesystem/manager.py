# Copyright (c) 2018 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import shell


def restartManager():
    restart = raw_input("    Restart Chroma Manager? (y/n)").lower()
    if restart in ['y', 'yes']:
        try:
            print "    Restarting Chroma Manager"
            shell.try_shell(['chroma-config', 'restart'])
        except Exception as e:
            print "    Error encountered while restarting the manager: %s" % e
            try_again = raw_input("    Try again? (y/n)").lower()
            if try_again in ['y', 'yes']:
                restartManager()
