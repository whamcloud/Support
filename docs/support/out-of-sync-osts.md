# Out of sync osts

Sometimes the ost_next_index will get out of sync. For example, you might have 5 OST's:

```
fs-OST0000
fs-OST0001
fs-OST0002
fs-OST0003
fs-OST0004
```

You might now try to add a new OST only to find that it fails because instead of creating fs-OST0005, it attempts to create fs-OST0003, which already exists. This is caused by a bug in the object caching in IML versions prior to 3.0. To fix this, you will need to:

1. Reset the next_ost_index counter in the `chroma_core_managedfilesystem` table to the appropriate value.
1. Update the mount point in the `chroma_core_managedtargetmount` table.
1. Update the `name`, `ha_label`, and `active_mount_id` in the `chroma_core_managedtarget` table.
1. Re-fromat the device using the command from the status page (but with the appropriate index).

The following video describes how to resolve the issue:

<div style="margin: 0 auto; width: 640px;">
  <iframe src="https://player.vimeo.com/video/301859928" width="640" height="360" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
</div>
