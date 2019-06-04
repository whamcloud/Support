# Create a Device Map

[Support Table of Contents](../TOC.md)

## Overview

It's useful to compare the device label to path mapping in an IML system to the actual output of `multipath -ll`. This will help identify
any mappings that are incorrectly specified within the IML system. The script below will not alter anything in the database but will accept
standard input in the form of: `<device label> <path>`. The easiest way to do this is to create a file containing all of this information.
The input can then be fed into device-mapper.py. For example:

```sh
# multipath-mapping.txt
3600a0980005b6afd000002ac5a573e25 mpatht
3600a0980005b6bff0000043d5a59458a mpathg
3600a0980005b6ac70000061451573f08 mpatha
```

## Usage

```sh
cat multipath-mapping.txt | python device-mapper.py
```

## Script

```python
#! /usr/bin/python

# Copyright (c) 2019 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys, os

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
sys.path.insert(0, "/usr/share/chroma-manager")
import settings
from chroma_core.models import Volume
from chroma_core.models import VolumeNode
from toolz import partial


def create_device_map():
    device_map = {}

    try:
        for line in sys.stdin:
            label, path = line.split(" ")
            device_map[label] = path
    except:
        print("Not able to read device map from stdin.")

    return device_map


def show_mpath(device_map, volume):
    try:
        volume_nodes = VolumeNode.objects.filter(volume_id=volume.id)
        print(
            "volume id: {} | label: {} | associated paths: {} | expected path: {}".format(
                volume.id,
                volume.label,
                ",".join(map(lambda x: x.path, volume_nodes)),
                device_map[volume.label],
            )
        )
    except:
        print("No matching volume node for {}".format(volume.label))


device_map = create_device_map()
map(partial(show_mpath, device_map), Volume.objects.all())
```

[top](#create-a-device-map)
