# Copyright (c) 2018 Intel Corporation. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import time
import shell


def __setMaintenanceMode(host, mode):
    try:
        print "   Setting maintenance mode to %s on %s." % (mode, host.fqdn)
        cmd = "pcs property set maintenance-mode=%s" % mode
        shell.try_remote_command(host.fqdn, cmd)
    except Exception as e:
        print "    Could not set the cluster to standby mode: %s" % e
        shell.cont()


def turnOnMaintenanceMode(host):
    __setMaintenanceMode(host, 'true')


def turnOffMaintenanceMode(host):
    __setMaintenanceMode(host, 'false')


def __setAgentState(host, action):
    try:
        print "    %s the agent on %s." % (action, host.fqdn)
        cmd = "service chroma-agent %s" % action
        shell.try_remote_command(host.fqdn, cmd)
    except Exception as e:
        print "    Could not stop the agent: %s" % e
        shell.cont()


def stopAgent(host):
    __setAgentState(host, 'stop')


def startAgent(host):
    __setAgentState(host, 'start')


def backupCurrentPacemakerConfig(host):
    try:
        print "    Backing up pacemaker config on %s" % host.fqdn
        ts = int(time.time())
        cmd = "cibadmin --query > /tmp/pacemaker_backup_%s" % ts
        shell.try_remote_command(host.fqdn, cmd)
    except Exception as e:
        print "    Could not backup the pacemaker config: %s" % e
        shell.cont()


def updatePacemakerConfig(host, cib, new_cib_location):
    try:
        print "    Copying %s to /tmp/selected_cib.xml and incrementing \
both epoch and admin epoch." % cib
        shell.try_remote_command(
          host.fqdn,
          """cat %s | sed "s/\\"/@@/g" | sed -r "s/(^<cib.+)(epoch=@@)([0-9]+)(.+)(admin_epoch=@@)([0-9]+)(.+)(>$)/echo \\"\\1\\2\\$((\\3+1))\\4\\5\\$((\\6+1))\\7\\8\\"/ge" | sed "s/@@/\\"/g" > %s""" % (cib, new_cib_location)  # noqa E501
        )
    except Exception as e:
        print "    Could not copy %s to %s. %s" % (cib, new_cib_location, e)
        shell.cont()


def applyNewPacemakerConfig(host, new_cib_location):
    try:
        print "    Applying new pacemaker config."
        shell.try_remote_command(
            host.fqdn,
            "cibadmin --replace --xml-file %s" % new_cib_location
        )
    except Exception as e:
        print "    Could not apply updated pacemaker configuration: %s" % e
        shell.cont()


def updatePacemaker(host, new_cib_location):
    update_pacemaker = raw_input(
      "    Update pacemaker for %s? (y/n)" % host.fqdn
    ).lower()

    if update_pacemaker in ['yes', 'y']:
        backupCurrentPacemakerConfig(host)

        cib = raw_input(
          "    Enter correct cib raw file location on %s. (Ex. /var/lib/\
pacemaker/cib/cib-24.raw):" % host.fqdn)
        updatePacemakerConfig(host, cib, new_cib_location)
        applyNewPacemakerConfig(host, new_cib_location)


def stopPacemaker(host):
    stop_service = raw_input(
        "    Stop pacemaker service on %s? (y/n)" % host.fqdn
    ).lower()
    if stop_service in ['y', 'yes']:
        print "    Stopping pacemaker on %s" % host.fqdn

        try:
            shell.try_remote_command(host.fqdn, 'service pacemaker stop')
        except Exception as e:
            print "    Could not stop pacemaker on %s: %s" % (host.fqdn, e)
            try_again = raw_input("    Try again? (y/n)").lower()
            if try_again in ['y', 'yes']:
                stopPacemaker(host)


def stopCorosync(host):
    stop_service = raw_input(
        "    Stop corosync service on %s? (y/n)" % host.fqdn
    ).lower()
    if stop_service in ['y', 'yes']:
        print "    Stopping corosync on %s" % host.fqdn

        try:
            shell.try_remote_command(host.fqdn, 'service corosync stop')
        except Exception as e:
            print "    Could not stop corosync on %s: %s" % (host.fqdn, e)
            try_again = raw_input("    Try again? (y/n)").lower()
            if try_again in ['y', 'yes']:
                stopCorosync(host)


def startPacemaker(host):
    start_service = raw_input(
        "    Start pacemaker service on %s? (y/n)" % host.fqdn
    ).lower()
    if start_service in ['y', 'yes']:
        print "    Starting pacemaker on %s" % host.fqdn

        try:
            shell.try_remote_command(host.fqdn, 'service pacemaker start')
        except Exception as e:
            print "    Could not start pacemaker on %s: %s" % (host.fqdn, e)
            try_again = raw_input("    Try again? (y/n)").lower()
            if try_again in ['y', 'yes']:
                startPacemaker(host)


def startCorosync(host):
    start_service = raw_input(
        "    Start corosync service on %s? (y/n)" % host.fqdn
    ).lower()
    if start_service in ['y', 'yes']:
        print "    Starting corosync on %s" % host.fqdn

        try:
            shell.try_remote_command(host.fqdn, 'service corosync start')
        except Exception as e:
            print "    Could not start corosync on %s: %s" % (host.fqdn, e)
            try_again = raw_input("    Try again? (y/n)").lower()
            if try_again in ['y', 'yes']:
                startCorosync(host)
