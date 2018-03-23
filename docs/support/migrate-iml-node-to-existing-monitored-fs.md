# Migrate an IML Manager configuration to a new server while preserving an existing monitored filesystem

[Support Table of Contents](TOC.md)

It may be necessary to migrate an IML manager node to a new server while still using an existing monitored filesystem with the existing MDS and OSS servers. In this case, the IML manager node will be re-installed on a new server and will be setup to communicate with the existing MDS and OSS servers.

## Performing The Migration

### Backup the database on the existing server

```shell
# login to the manager node as root
su -l postgres
pg_dump -U chroma chroma > /tmp/db_backup_xxx.sql
exit
```

[top](#migrate-an-iml-manager-configuration-to-a-new-server-while-preserving-an-existing-monitored-filesystem)

### Setup server networking.

The new server will need to communicate with the existing MDS and OSS nodes. Ensure the following:
  * New IML Server Node:
    * Verify that all MDS and OSS nodes are defined with the correct hostname and IP address in the name resolution system (i.e. /etc/hosts, DNS, NIS, etc.).
  * Existing MDS and OSS nodes
    * Verify that the IP address and hostname for the new IML server are reflected in the name resolution system (i.e. /etc/hosts, DNS, NIS, etc.).

[top](#migrate-an-iml-manager-configuration-to-a-new-server-while-preserving-an-existing-monitored-filesystem)

### Download and Install IML.

[top](#migrate-an-iml-manager-configuration-to-a-new-server-while-preserving-an-existing-monitored-filesystem)

### Run the database import script.

Upload the sql file from step 1 and the [import database script](scripts/import-customer-database.md) onto the new IML server. Once uploaded, log into the new IML server and execute the script, passing the sql filename as an argument:
```shell
chmod +x import_database.py
./import_database.py db_backup_xxx.sql
```

This will import the existing database file onto the new IML server and restart the chroma-manager service. 

[top](#migrate-an-iml-manager-configuration-to-a-new-server-while-preserving-an-existing-monitored-filesystem)

### Run the sha256 migration script.

Download, extract, and run the appropriate version of the sha-256 migration script:
* [sha-256-migration-IML-2.4.x](scripts/sha-256-migration/sha-256-browser-migration-2.4.x.v1.tar.gz)
* [sha-256-migration-IML-3.x.x](scripts/sha-256-migration/sha-256-browser-migration-3.x.x.v1.tar.gz)

```shell
tar xvf sha-256-browser-migration-3.x.x.v1.tar.gz
cd sha-256-browser-migration-3.x.x.v1
./main
```

You should have output similar to the following:
```
Creating manager certificates:
    - Backing up certificates and pem files to /var/lib/chroma/backup_1521790193
    - Generated Private Key: /var/lib/chroma/authority.pem
    - Created Authority Certificate using sha256: /var/lib/chroma/authority.crt
    - Generated Private Key: /var/lib/chroma/manager.pem
    - Created Manager Certificate using sha256: /var/lib/chroma/manager.crt
    - Updating /usr/share/chroma-manager/chroma_core/services/http_agent/crypto.py on manager node.

Migrating certificates to mds1.lfs.local:
    - Backing up certificates on mds1.lfs.local
    - Uploading /var/lib/chroma/authority.crt to mds1.lfs.local:/var/lib/chroma/authority.crt
    - Generating private key on mds1.lfs.local
    - Creating new certificate on mds1.lfs.local
    - Restarting Agent on mds1.lfs.local

Migrating certificates to mds2.lfs.local:
    - Backing up certificates on mds2.lfs.local
    - Uploading /var/lib/chroma/authority.crt to mds2.lfs.local:/var/lib/chroma/authority.crt
    - Generating private key on mds2.lfs.local
    - Creating new certificate on mds2.lfs.local
    - Restarting Agent on mds2.lfs.local

Migrating certificates to oss1.lfs.local:
    - Backing up certificates on oss1.lfs.local
    - Uploading /var/lib/chroma/authority.crt to oss1.lfs.local:/var/lib/chroma/authority.crt
    - Generating private key on oss1.lfs.local
    - Creating new certificate on oss1.lfs.local
    - Restarting Agent on oss1.lfs.local

Migrating certificates to oss2.lfs.local:
    - Backing up certificates on oss2.lfs.local
    - Uploading /var/lib/chroma/authority.crt to oss2.lfs.local:/var/lib/chroma/authority.crt
    - Generating private key on oss2.lfs.local
    - Creating new certificate on oss2.lfs.local
    - Restarting Agent on oss2.lfs.local

Restarting Manager:
Stopping daemons
Starting daemons
```

[top](#migrate-an-iml-manager-configuration-to-a-new-server-while-preserving-an-existing-monitored-filesystem)

### Refresh the browser and accept the certificate. Make sure the browser is pointed at the home page:
```
https://<hostname|IP>/ui/
```

### Update the MDS and OSS nodes to point to the new IML server

**If the hostname did not change then this step is not needed.** In the event that the hostname did change, the MDS and OSS nodes need to be configured such that they point to the new hostname. To accomplish this, the chroma settings on each of the server nodes will need to be updated. Replace `<hostname>` in the command below with the hostname of the IML server and run this command on each of the MDS and OSS nodes.
```shell
echo "{\"url\": \"https://<hostname>:443/agent/\"}" > /var/lib/chroma/settings/c2VydmVy
```

Note that the filename `c2VydmVy` is base64 encoded and when decoded will read, `server`. 

Restart the chroma-agent service after making this change:
```shell
systemctl restart chroma-agent.service
```

Repeat this process for each of the server nodes. 

[top](#migrate-an-iml-manager-configuration-to-a-new-server-while-preserving-an-existing-monitored-filesystem)