# IML Responds With 502

[Support Table of Contents](TOC.md)

If IML responds with a 502 it means that a manager service is not responding as expected. This could be caused by a number of issues. The items below list some troubleshooting tips when encountering this error. In addition to these tips, it will be helpful to look through the logs under `/var/log/chroma/` on the manager node. These logs may contain error messages, tracebacks, or other useful information. Finally, it may be helpful to collect IML diagnostics by running `iml-diagnostics`. This will generate a compressed file containing all of the logs and much more that can aid in troubleshooting the problem.

## Check the load on the node

It's possible that the process load is too high or the memory is exhausted on the manager node. You can check this by sshing into and running `top` on the manager node. Once loaded, check the process load and the memory pressure (in particular, the amount of virtual memory taking place).

## Job Scheduler Throttling

IML 3.0.x has a known issue in which RPC throttling in the job scheduler skyrockets. Seeing a 502 when running this version of IML is a good sign that this is taking place. Look for the following in the job_scheduler.log:

```
[2018-12-20 08:31:55,691: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2344
[2018-12-20 08:31:56,360: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2345
[2018-12-20 08:31:56,523: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2346
[2018-12-20 08:31:56,555: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2347
[2018-12-20 08:31:57,250: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2348
[2018-12-20 08:31:58,191: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2349
[2018-12-20 08:31:59,038: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2350
[2018-12-20 08:31:59,046: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2351
[2018-12-20 08:31:59,128: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2352
[2018-12-20 08:31:59,351: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2353
[2018-12-20 08:32:00,137: INFO/rpc] Throttled rpc to get_locks throttled rpcs=2354
```

If the rpc count is climbing then IML needs to be upgraded.
