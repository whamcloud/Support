# Target Operation Error: Unable to find the secondary server for **target-HA**

[Support Table of Contents](TOC.md)

## Intro

This error will occur if a resource constraint's name does not match properly in the pacemaker configuration.

## Description

In general, pacemaker allows for arbitrary names when defining resource constraints in the pacemaker config. IML, however, uses the following regex when looking for secondary servers:

```regex
\s+:\s+Node\s+([^\s]+)\s+\(score=[^\s]+ id=${ha-label}-[primary|secondary]\)
```

This means that the id **must** be in the format:

```ruby
${ha-label}-primary
# or
${ha-label}-secondary
```

The "Unable to find the secondary server for `target-HA`" error message indicates that the resoruces constraint is not named properly. A correct resource constraint definition looks like this:

```xml
<rsc_location id="fs-OST0000_9e8c08-primary" node="oss2.local" rsc="fs-OST0000_9e8c08" score="20"/>
<rsc_location id="fs-OST0000_9e8c08-secondary" node="oss1.local" rsc="fs-OST0000_9e8c08" score="10"/>
```

## Summary

To resolve this issue, simply update the resource location id's such that their format is correct. The error message should no longer occur once all resource locations have been updated in the pacemaker config.

[top](#target-operation-error-unable-to-find-the-secondary-server-for-target-ha)
