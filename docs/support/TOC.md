# Support Table of Contents

This is the Support table of contents. Quickly find an issue that has been solved in the past and discover how it was resolved.

[Common Troubleshooting And Tips](common-troubleshooting-tips.md)

---

## Support Docs

- [Out of Sync OST's](out-of-sync-osts.md)
  - Sometimes the OST index gets out of sync and you can no longer add an OST to your filesystem because it attempts to pick a name that already exists. Learn how to reset the OST count index.
- [Volumes Not Displaying Properly](volumes-not-displaying-properly.md)
  - If the state of the database no longer reflects the state of the system it could cause your new disks to not show up on the
    volumes page. It could also show incorrectly configured HA data for your volumes. Learn how to identify such a case and how to
    resolve it so that all volumes are reflected correctly.
- [(Force) Lowering an Alert](lower-alert.md)
  - Sometimes there can be an alert that won't get lowered despite the condition that it's alerting about not being true.
- [Cannot Add OST](cannot-add-osts.md)
  - If an OST can't be added there could be several reasons. Check here to see common reasons and their solutions.
- [Re-add managed ZFS filesystem (3.1.x only)](re-add-managed-zfs-fs.md)
  - If you need to re-add a managed ZFS filesystem over an existing configuration. This procedure is meant for a fs that has the same targets and pool / dataset names, but different guids.
- [Migrate an IML Manager configuration to a new server while preserving an existing monitored filesystem](migrate-iml-node-to-existing-monitored-fs.md)
  - Describes how to move an IML manager node to a different server while still using the existing MDS and OSS nodes.
- [IML Installation Fails](cannot-install-iml.md)
  - Provides a list of things to check when IML fails to install.
- [Build Lustre RPMs against Mellanox](build-lustre-rpms-against-mellanox.md)
  - Instructions on how to build Lustre rpm's against mellanox
- [IML Version Matrix](version-matrix.md)
  - Matrix showing Lustre/IML versions along with the required OS version
- [DatabaseError: current transaction is aborted, commands ignored until end of transaction block](database-error-transaction-aborted.md)
  - How do you fix, "DatabaseError: current transaction is aborted, commands ignored until end of transaction block" when loading the IML GUI?
- [Target Operation Error: Unable to find the secondary server for `target-HA`](target-operation-error.md)
  - What causes "Unable to find the secondary server for \*" when attempting to fail over a target?
- [IML Responds with 502](iml-responds-with-502.md)
  - What can cause IML to respond with a 502 when loading the page?
- [How To Upgrade IML](how-to-upgrade-iml.md)
  - Learn how to upgrade IML with visual steps.

---

## Scripts

- [Import Customer's Database](scripts/import-customer-database.md)
  - Automated script to import a customer's database
- [Sha-256-Migration for IML@2.4.x](scripts/sha-256-migration/sha-256-migration-2.4.x.md)
  - Migrate certificates across cluster for IML@2.4.x
- [Sha-256-Migration for IML@3.x.x](scripts/sha-256-migration/sha-256-migration-3.x.x.md)
  - Migrate certificates across cluster for IML@3.x.x
- [Restore a removed filesystem](scripts/restore-filesystem/restore-filesystem.md)
  - Restore a filesystem that was accidentally removed from IML
- [Create a Device Map](scripts/device-mapper.md)
  - Create a device label to path map and compare the systems mapping to multipath output
