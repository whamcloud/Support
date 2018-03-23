<a name="top"></a>
[Support Table of Contents](TOC.md)
# Migrating an IML node to and existing ZFS Monitored Filesystem

It may be necessary to migrate an IML manager node to a new server while still using an existing ZFS Monitored filesystem with the existing MDS and OSS servers. In this case, the IML manager node will be re-installed on a new server and will be setup to communicate with the existing MDS and OSS servers.

## Performing The Migration

### Backup the database on the existing server

There are two backup methods:
* Backup the entire database:
```
1. ssh into the manager node as root
2. su -l postgres
3. pg_dump -U chroma chroma > /tmp/db_backup_xxx.sql
4. exit
```
* Backup the database without metric data (Useful if backing up the entire database is too large):
```
1. ssh into the manager node as root
2. su -l postgres
3. pg_dump -U chroma -F p -w -T 'chroma_core_series*' -T 'chroma_core_sample*' -T 'chroma_core_logmessage*' -f /tmp/db_backup_xxx.sql
4. exit
```

[top](#top)

### Setup server networking.

The new server will need to communicate with the existing MDS and OSS nodes. Ensure the following:
  * New IML Server Node:
    * Verify that all MDS and OSS nodes are defined with the correct hostname and IP address in the /etc/hosts file. 
  * Existing MDS and OSS nodes
    * Verify that the IP address and hostname for the new IML server are reflected in the /etc/hosts file

[top](#top)


### Setup ssh between the new IML server and the existing MDS and OSS nodes

It is important that the IML manager node can communicate with the existing MDS and OSS nodes without having to enter a password. SSH keys should be setup to ensure that the manager node can ssh into any of the MDS/OSS nodes without having to specify a password. Likewise, all MDS and OSS nodes should be able to ssh into the new IML manager node. 

[top](#top)

### Download and Install IML.

[top](#top)

### Run the database import script.

SCP the sql file from step 1 and the [import database script](scripts/import-customer-database.md) onto the new IML server. Once uploaded, ssh into the new IML server and execute the script, passing the sql filename as an argument:
```
scp import_database.py root@<new-iml-server-ip>:~
scp chromadb_backup_xxx.sql root@<new-iml-server-ip>:~
ssh root@<new-iml-server-ip>
[~]# chmod +x import_database.py
[~]# ./import_database.py db_backup_xxx.sql
```

This will import the existing database file onto the new IML server and restart the chroma-manager service. 

[top](#top)

### Run the sha256 migration script.

Download, extract, and run the appropriate version of the sha-256 migration script:
* [sha-256-migration-IML-2.4.x](scripts/sha-256-migration/sha-256-browser-migration-2.4.x.v1.tar.gz)
* [sha-256-migration-IML-3.x.x](scripts/sha-256-migration/sha-256-browser-migration-3.x.x.v1.tar.gz)

```
scp sha-256-browser-migration-3.x.x.v1.tar.gz root@<new-iml-server-ip>:~
ssh root@<new-iml-server-ip>
[~]# tar xvf sha-256-browser-migration-3.x.x.v1.tar.gz
[~]# cd sha-256-browser-migration-3.x.x.v1
[~/sha-256-browser-migration-3.x.x.v1]# ./main
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

[top](#top)

### Refresh the browser and accept the certificate. Make sure the browser is pointed at the home page:
```
https://<hostname|IP>:443/ui/
```

### Update the MDS and OSS nodes to point to the new IML server

**If the hostname did not change then this step is not needed.** In the event that the hostname did change, the MDS and OSS nodes need to be configured such that they point to the new hostname. To accomplish this, the chroma settings on each of the server nodes will need to be updated:
```
# Example for MDS1
cd /var/lib/chroma/settings
for i in `ls`
do
   echo "$i: `echo \"$i\" | base64 --decode`"
done
```

This will decode each of the filenames and print their content:
```
bGFzdF9kZXRlY3Rfc2Nhbl90YXJnZXRfZGV2aWNlcw==: last_detect_scan_target_devices
c2VydmVy: server
cHJvZmlsZQ==: profile
YWdlbnQ=: agent
```

The file that maps to `server` needs to be updated to point to the new IML server hostname. For example, if the hostname changed from `adm.lfs.local` to `adm-centos72.lfs.local`,`c2VydmVy` would be updated as follows:
```
{"url": "https://adm-centos72.lfs.local:443/agent/"}
```

Restart the chroma-agent service after making this change:
```
systemctl restart chroma-agent.service
```

Repeat this process for each of the server nodes. 

[top](#top)