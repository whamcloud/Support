# Re-add a managed ZFS filesystem

This procedure allows an operator to replace an existing managed mode install with a new ZFS backed Lustre fs. It is a prereq that the pool / dataset / mountpoints are the same as the previous fs.

## In the GUI

1.  Stop the FS including mgt via the GUI.

## On the manager node

1.  stop the manager

    ```shell
    chroma-config stop
    ```

## On each storage node

1.  Stop the agent:

    ```shell
    service chroma-agent stop
    ```

1.  Activate maintenance mode:

    ```shell
    crm configure property maintenance-mode=true
    ```

1.  Navigate to `/var/lib/chroma/targets` and run:

    ```shell
    for file in `ls`
      do
        echo -en '\n'
        echo file: $file
        echo uuid: `echo $file | base64 --decode`
        echo contents: `cat $file`
        echo -en '\n'
      done
    ```

    This should output something like:

    ```shell
    file: MzAzMzk2NzE3NDk0MDI4NzQ1MQ==
    uuid: 3033967174940287451
    contents: {"device_type": "zfs", "bdev": "oss1/fs-OST0000", "backfstype": "zfs", "mntpt": "/mnt/fs-OST0000"}

    file: NTUwMjY3NjQ5MjQ4ODQ3Njgw
    uuid: 550267649248847680
    contents: {"device_type": "zfs", "bdev": "oss2/fs-OST0001", "backfstype": "zfs", "mntpt": "/mnt/fs-OST0001"}
    ```

    Each entry represents a target that can be mounted on this node. Note the `uuid` and `bdev` fields to determine which files need updating.

1.  For each dataset with a new guid, update the base64 encoded filename. To get the new filename for a target:

    ```shell
    zfs get -Hpo value guid POOL_DS_PATH | xargs echo -n | base64
    ```

    make sure to overwrite the old base64 filename with the new one.

1.  Update the corosync resource target attribute. To see the resources:

    ```shell
    pcs resource show --full
    ```

    This will output something like:

    ```shell
    Resource: fs-OST0000_465bfc (class=ocf provider=chroma type=Target)
     Attributes: target=3033967174940287451
     Meta Attrs: target-role=Started
      Operations: monitor interval=5 timeout=60 (fs-OST0000_465bfc-monitor-5)
                  start interval=0 timeout=300 (fs-OST0000_465bfc-start-0)
                  stop interval=0 timeout=300 (fs-OST0000_465bfc-stop-0)
    Resource: fs-OST0001_c0e696 (class=ocf provider=chroma type=Target)
     Attributes: target=550267649248847680
     Meta Attrs: target-role=Started
     Operations: monitor interval=5 timeout=60 (fs-OST0001_c0e696-monitor-5)
                 start interval=0 timeout=300 (fs-OST0001_c0e696-start-0)
                 stop interval=0 timeout=300 (fs-OST0001_c0e696-stop-0)
    ```

    Note the target attribute. This is what we want to update with a new guid. To update:


    ```shell
    crm_resource --resource RESOURCE_NAME_HERE --set-parameter target --parameter-value NEW_GUID_HERE
    ```

    where `NEW_GUID_HERE` is the output of `zfs get -Hpo value guid POOL_DS_PATH` for the relevant dataset.

## Back on the manager node

1.  Enter a db shell:

    ```shell
        python /usr/share/chroma-manager/manage.py dbshell
    ```

1.  Run the following SQL commands to update guids in the db:

    ```sql
    update chroma_core_managedtarget
        set uuid = 'NEW_GUID'
        where uuid = 'OLD_GUID'
        and not_deleted = 't';

    update chroma_core_storageresourcerecord
        set storage_id_str = '["NEW_GUID"]'
        where storage_id_str = '["OLD_GUID"]';

    update chroma_core_storageresourceattributeserialized
        set value = '"NEW_GUID"'
        where value = '"OLD_GUID"';
    ```

    Note that `OLD_GUID` and `NEW_GUID` are the only parts of the command that should change. Everything else, including quotes and brakets should remain.

1.  Start the manager:

    ```shell
        chroma-config start
    ```

## On each storage node

1.  Deactivate maintence mode:

    ```shell
    crm configure property maintenance-mode=false
    ```

1.  Start the agent:

    ```shell
    service chroma-agent start
    ```

Finally, wait a few minutes and start the filesystem via the GUI. You should see the targets mount as expected.
