# Out of sync osts

Sometimes IML will think that the ost index is different thant the number of OST's you have. For example, you might have 5 OST's:
```
fs-OST0000
fs-OST0001
fs-OST0002
fs-OST0003
fs-OST0004
```

You might now try to add a new OST only to find that it fails because instead of creating fs-OST0005, it attempts to create fs-OST0003, which already exists. To fix this, you simply need to reset the counter in the `chroma_core_managedfilesystem` table. Here is a script that will automate this for you.

```
#! /usr/bin/python

import sys, os
import string

sys.path.append('/usr/share/chroma-manager')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

from chroma_core.models import ManagedFilesystem

ost_new_index = 5

filesystem = ManagedFilesystem.objects.get(name='fs')

print "current ost next index: %s" % filesystem.ost_next_index

print "Setting ost next index to %s" % ost_new_index
filesystem.ost_next_index = ost_new_index
filesystem.save()

print "ost next index saved! New value is: %s" % filesystem.ost_next_index

print "Process completed."
```

In this case, the index will be set to 5.