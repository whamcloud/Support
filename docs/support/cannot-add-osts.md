<a name="top"></a>
[Support Table of Contents](TOC.md)
# Cannot Add OST to IML in Managed Mode

There may be several factors preventing an OST from being added to IML. The below sections will help identify known issues and their solutions. 

## TOC
- [Attempting to Add an OST yields in: mkfs.lustre: path apparently does not exist](#case1)
  - [Problem](#case1-problem)
  - [Analysis](#case1-analysis)
  - [Solution](#case1-solution)

<a name="case1"></a>
### Attempting to Add an OST yields in: mkfs.lustre: <path> apparently does not exist



<a name="case1-problem"></a>
#### Problem:
The path in which IML is trying to add the OST does not exist on the OSS. This may happen in the event that multipath is being used and an alias is being created. 

[top](#top)

<a name="case1-analysis"></a>
#### Analysis:
First, identify if multipath is being used. If it is, get the devlinks for the disk when multipath is on and when it is off:

```
oss# udevadm trigger
oss# udevadm info --query=property --name=<device name>
```

Look for a property called "DEVLINKS". You might find data that looks similar to this:
```
# Without multipath alias
DEVLINKS=/dev/mapper/360060e8016641330000166130000c021 /dev/disk/by-id/dm-name-360060e8016641330000166130000c021 /dev/disk/by-id/dm-uuid-mpath-360060e8016641330000166130000c021 /dev/disk/by-uuid/05fa54cd-7d12-4090-9c8f-53441f158d12 /dev/disk/by-label/home-OST0001 /dev/block/253:15

# With multipath alias
DEVLINKS=/dev/mapper/ost01 /dev/disk/by-id/dm-name-ost01 /dev/disk/by-id/dm-uuid-mpath-360060e8016641330000166130000c021 /dev/disk/by-uuid/05fa54cd-7d12-4090-9c8f-53441f158d12 /dev/disk/by-label/home-OST0001 /dev/block/253:15
```

The problem is more than likely that IML is attempting to add the target using `/dev/mapper/360060e8016641330000166130000c021` as the path. This path no longer exists after multipath creates an alias. 

[top](#top)

<a name="case1-solution"></a>
#### Solution:
The OSS nodes need to be updated with the correct path. Navigate to `/var/lib/chroma/targets` (the config store) on the OSS node and look at the data for each target:

```
for file in `ls`
  do
    echo file: $file
    echo uuid: `echo $file | base64 --decode`:
    cat $file
    echo
  done
```

This will result in data similar to the following:
```
file: ef98a76321.....
uuid: 05fa54cd-7d12-4090-9c8f-53441f158d12:
{"target_name": "home-OST0001", "bdev": "/dev/mapper/360060e8016641330000166130000c021", "backfstype": "ext4", "mntpt": "/mnt/home-OST0001"}
...
```

Update the `bdev` property with the alias path that multipath has defined and save the file:
```
{"target_name": "home-OST0001", "bdev": "/dev/mapper/ost01", "backfstype": "ext4", "mntpt": "/mnt/home-OST0001"}
```
Update each target file such that the bdev path is set to the targets corresponding multipath alias. Within a few minutes IML should pick up the change on the filesystem detail page. It is important to note that IML uses longpolling to gather disk information from agent nodes so it could take up to 10 minutes for this new information to propagate up to the manager. Once it does, the target should be available to add to the filesystem and failover services should work as expected. 

[top](#top)