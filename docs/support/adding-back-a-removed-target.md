# Support - Adding Back Removed Targets

## Overview
There may be times in which an OST is removed by accident and needs to be added back into the filesystem. To do this,
the OST will need to be mounted and IML will need to be notified of its existence.

## Example
A customer just removed 2 of their OST's (lustre-OST0005, lustre-OST0006) by mistake and needs to add them back in. 

## Solution
The first thing to do is mount both of the OST's that were removed using the `mount -t lustre /dev/disk/by-id/ata-VBOX_HARDDISK_OST5PORT600000000000 /mnt/lustre-OST0005` command. Lustre will now
be able to use these ost's but IML doesn't know anything about them. In fact, running `pcs resource show` on the oss node 
will show that it knows nothing about these two OST's. That's because when an OST is removed using IML it removes the resource
from pacemaker. Luckily, pacemaker makes a backup of every change (up to 100 files). You can get all of the backup files in 
one compressed file using the following command:

```
tar -czvf cibs.tar.gz -C /var/lib/pacemaker/cib .
```

Before updating pacemaker, the database should be updated to show the targets that were removed. It so happens that when a change is made to IML,
the entries that were removed were NOT deleted from the database. Instead, these entries have a `not_deleted` flag, indicating whether or not the
target is active. This value can be updated accordingly:

```
update chroma_core_managedtarget set state='mounted', not_deleted=True, active_mount_id=10 where id=5;
```

This will make the target who's id is 5 (lustre-OST0005 in this case) display on the filesystem detail page again. Note that the active_mount_id must
be set but it doesn't have to be set to the correct value just yet. The system will take care of that when it is time; this will simply put the target
back on the screen.

Next, the pacemaker configuration needs to be updated. The goal is to locate the raw file in the pacemaker backup that contained the resources just before they were removed. `grep` in conjunction with timestamps is an excellent tool in locating the correct raw file. Once the file has been found, the resources
can be copied into the current cib.xml. In this example, the correct file is `/va/lib/pacemaker/cib/cib-64.raw`. Now that the file has been located, make 
a backup of the current file and add the resources in manually. Alternatively, if no other changes have been made since the OST's were removed, the current
file can simply be replaced by cib-64.raw. It's also important to note that both the epoch and admin epoch values must be changed whenever making a 
manual change like this.

```
cibadmin --query --local > ~/cib.bk
cp /var/lib/pacemaker/cib/cib-64.raw ~/local.xml # This is the backup containing the deleted resources
vim ~/.local.xml # Increment both epoch and admin epoch values
cibadmin --replace --xml-file ~/local.xml # replace the current configuration with the backup containing the removed resources
```

Restart the corosync and pacemaker services on each of the OSS's where the change is being made.

```
systemctl stop corosync.service
systemctl stop pacemaker.service
systemctl start corosync.service
systemctl start pacemaker.service
```

Pacemaker now knows about the resources and it will attempt to manage the two OST's, but there is a problem; it can't manage them if they aren't started.
Doing a quick `pcs resource` will show that the OST's are not started. It's also important to take note of the provider: `ocf::chroma:Target`. This is the 
script that manages the resource and it can be located at `/usr/lib/ocf/resource.d/chroma/Target`. Looking at the script will show that the `Start` operation
runs a command similar to this:

```
chroma-agent target_running --uuid <serial>
```

The next logical step is to see the result of running this command on the disk associated with the OST. The serial can be found in `/dev/disk/by-uuid` or by
checking the mount information. Trying to run this command against the uuid of the target disk will result in an exception:

```
Exception getting target config: '"Invalid key 'xxx' for config section 'targets'"'
```

This ultimately means that the resource can't be managed because the target hasn't been registered and thus it cannot be found when checking if the target 
is running. To fix this, the target needs to be registered with the store. This can be done by running the `register_target` and `configure_target_store` commands:

```
chroma-agent register_target --device_path /dev/disk/by-id/ata-VBOX_HARDDISK_OST5PORT600000000000 --mount_point /mnt/fs-OST0005 --backfstype ldiskfs

chroma-agent configure_target_store --device /dev/disk/by-id/ata-VBOX_HARDDISK_OST5PORT600000000000 --uuid f0f1e759-4de9-4d99-8fe7-d935a10e837a --mount_point /mnt/fs-OST0005 --backfstype ldiskfs --device_type linux

# Make sure the target is mounted if not already
mount -t lustre /dev/disk/by-id/ata-VBOX_HARDDISK_OST5PORT600000000000 /mnt/fs-OST0005
```

The entry should now appear in the store on the OSS:
```
cd /var/lib/chroma/targets/
ls -la
...
# -rw------- 1 root root  143 Jan 12 12:59 ZWUzYjFjODYtYmQ3Ny00MGFhLTkwZDgtZTc2YmJjZjZkODFj
```

The timestamp will indicate the file that was added to the store. It can be checked by running it against `base64`:

```
echo ZWUzYjFjODYtYmQ3Ny00MGFhLTkwZDgtZTc2YmJjZjZkODFj | base64 --decode
# ee3b1c86-bd77-40aa-90d8-e76bbcf6d81c
```

This is the uuid of the resource to be added. Now that the key is registered in the store, the last step is to go to the filesystem detail page in the gui and select the dropdown next to the broken target and select `Start`. The start command should now run successfully and should now be managed by pacemaker. Running `pcs resource show` should indicate that the target is now started and being managed. The `active_mount_id` should also be updated in the database to reflect the correct mount id. Note that these steps can be repeated for each OST that was removed. 
