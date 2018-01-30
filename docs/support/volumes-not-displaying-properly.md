# Support - Volumes Not Displaying Properly

## Overview
Sometimes the IML state is no longer in sync with the actual state of the disks and filesystem. In the case
of volumes, this could mean that volumes that are available may not display at all on the volumes page. It 
could also mean that volumes may display with incorrectly configured HA properties. To resolve this kind of 
issue, you will need to manually update the volumes and their associated storage resources such that they are
synced correctly.

## Example
A customer just expanded 6 new disks on their system, but only three of these disks display on the volume page:


| Volume Name   | Primary Server   | Failover Server   | Size   | Status  |
| -------------:|:----------------:|:-----------------:|:------:|:-------:|
| ...fb63       | oss1             | ----              | 58.2T  | Yellow  |
| ...fac2       | oss1             | oss2              | 55.4T  | Green   |
| ...dc68       | ----             | ----              | 53.7T  | Red     |

Not only are only three volumes missing, but of the three that are displayed, two of them indicate that HA is
not configured. In this case, the servers are perfectly capable of working together as an HA pair, the state 
of the database does not reflect the reality of the system. To correct this, several tables will need to be
analyzed and updated.

## Solution

1. ssh into the IML manager node
2. cd /usr/share/chroma-manager
3. python manage.py dbshell

This will establish a connection to the postgres database. The tables of interest are as follows:
1. chroma_core_volume
2. chroma_core_volumenode
3. chroma_core_storageresourcerecord

### Fixing incorrectly mapped volume nodes

To understand this problem, it is important to understand how these three tables relate. chroma_core_volume contains all volumes in the 
system as well as their labels. For example:

```chroma_core_volume
 id | storage_resource_id |      size      |               label               | filesystem_type | not_deleted
----+---------------------+----------------+-----------------------------------+-----------------+-------------
 58 |                 692 | 32001985871872 | ...fb63                           | ext4            | t
 ```

 This is one of the volumes listed on the volumes page (fb63). This looks fine so far, but digging deeper we will see a problem. Notice
 the volume has an id of 58. A simple query will bring up the volume node where the volume has an id of 58:

 ```chroma_core_volumenode
 id  | volume_id | host_id |                          path                          | storage_resource_id | primary | use | not_deleted
-----+-----------+---------+--------------------------------------------------------+---------------------+---------+-----+-------------
 211 |        58 |      16 | /dev/mapper/mpatho                                     |                1255 | f       | f   | t
 115 |        58 |      15 | /dev/mapper/mpathg                                     |                     | f       | t   |
 121 |        58 |      16 | /dev/mapper/mpathh                                     |                 784 | t       | t   |
 ```

 It's pretty clear there is a problem with this configuration. First, it's important to know which path this volume node should be on.
 There is a mixture of mpatho, mpathg, and mpathh. In this case, there should be two active entries on mpathn. The paths are clearly 
 wrong, so the question becomes, how should they be updated? An attempt to update that path will clearly not work as there are 
 duplicate key constraints. The only other option is to explore the associated storage resource. 

Looking at the big picture, the disk with a label of ...fb63 needs to be on a path of /dev/mapper/mpathn. Currently, the only active volume 
node associated with ...fb63 is volume_node 211, with a path of /dev/mapper/mpatho; The other two entries are deleted. One of the first 
options is to look and see what is assigned to mpathn in the volumes_node table. 

```
 id  | volume_id | host_id |                          path                          | storage_resource_id | primary | use | not_deleted
-----+-----------+---------+--------------------------------------------------------+---------------------+---------+-----+-------------
 198 |        77 |      15 | /dev/mapper/mpathn                                     |                1241 | t       | t   | t
 207 |        53 |      16 | /dev/mapper/mpathn                                     |                1251 | f       | f   | t
```

It's clear that mpathn should be assigned to volume_id 58, but before updating, it's imporant to check and see what volume 77 and 53 are.
```
 id | storage_resource_id |      size      |               label               | filesystem_type | not_deleted
----+---------------------+----------------+-----------------------------------+-----------------+-------------
 77 |                1162 | 63965249929216 | 3600a0980006355f3000004e05a5efa2c |                 | t
 53 |                 697 | 32001985871872 | 3600a0980006355f30000022454b3c10b | ext4            | t
```

Looks like both 77 and 53 are in use since they are not deleted; But what are they? It just so happens that in this example,
77 has label ...fa2c, which is one of the other new volumes. It obviously doesn't have the right information either because 
it shouldn't have a path of /dev/mapper/mpathn. It should have been /dev/mapper/mpatho. Therefore, the `volume_id` label
can be updated for volumenode 198 from 77 to 58:
```
update chroma_core_volumenode set volume_id=58 where id=77;
```
...fb63 now has one of the volume nodes set correctly, but it still needs its HA pair. Chances are that volumenode 207 could also 
be updated to 58. It just dependes on what is on volume 53. If volume 53 is one of the new volumes (chances are that it is), then 
it's volume_id should also be updated to 58. Later, volume 53 and 77 will both be addressed in the same way such that the correct volume node
is mapped to it. 

There may be times where there is more involved then simply updating the volume_id in the volumenode table. Keep in mind that 
the storage_resource_id should contain the same path information that is being displayed in the volume node. Going back to the 
exmaple for ...fb63, there should be two active volume nodes whose paths point to /dev/mapper/mpathn. Each of these nodes should
have a corresponding storage resource record. Looking at each resource record, it should be clear that the volume nodes path
matches the storageresourcerecord's storage_id_str:

```
select * from chroma_core_storageresourcerecord where storage_id_str = '["/dev/mapper/mpathn"]';
 id  | resource_class_id |                          storage_id_str                          | storage_id_scope_id | alias
-----+-------------------+------------------------------------------------------------------+---------------------+-------
1241 |                 2 | ["/dev/mapper/mpathn"]                                           |                 682 |
1251 |                 2 | ["/dev/mapper/mpathn"]                                           |                 749 |
```

If the path doesn't match the storage_id_str then you may need to search for the correct storageresourcerecord that does 
match the path and update the storage_resource_id in the storagenode accordingly. 

### Fixing Volume Nodes That Are Missing

Locating volume nodes that are missing is quite simple. Simply look for the volume node with the label you want and make sure
it is not deleted. For example:

```
 id | storage_resource_id |      size      |               label               | filesystem_type | not_deleted
----+---------------------+----------------+-----------------------------------+-----------------+-------------
 19 |                     |    10737418240 | 36b083fe000c00c010000022554b2c96b |                 |
 ```

 ...c96b is a new volume that should be displayed, but it is not. To resolve this, simply update the "not_deleted" 
 property:

 ```
 update chroma_core_volume set not_deleted=True where id=19;
 ```

 The volume should then appear on the volumes page.
 