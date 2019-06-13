# Job scheudler and http logs show KeyError: connection.blocked

[Support Table of Contents](TOC.md)

## Problem

The following error may occurr in the job-scheduler or http log on the manager node:

```bash
 backtrace: Traceback (most recent call last):

  File "/usr/share/chroma-manager/chroma_core/services/__init__.py", line 73, in run
    self.service.run()

  File "/usr/share/chroma-manager/chroma_core/services/job_scheduler/agent_rpc.py", line 108, in run
    HttpAgentRpc().reset_plugin_sessions(AgentRpcMessenger.PLUGIN_NAME)

  File "/usr/share/chroma-manager/chroma_core/services/rpc.py", line 549, in <lambda>
    return lambda *args, **kwargs: self._call(name, *args, **kwargs)

  File "/usr/share/chroma-manager/chroma_core/services/rpc.py", line 565, in _call
    result = rpc_client.call(request, rpc_timeout)

  File "/usr/share/chroma-manager/chroma_core/services/rpc.py", line 359, in call
    self._send(connection, request)

  File "/usr/share/chroma-manager/chroma_core/services/rpc.py", line 351, in _send
    producer.publish(request, serializer="json", routing_key=self._request_routing_key, delivery_mode=1)

  File "/usr/lib/python2.7/site-packages/kombu/messaging.py", line 181, in publish
    exchange_name, declare,

  File "/usr/lib/python2.7/site-packages/kombu/messaging.py", line 203, in _publish
    mandatory=mandatory, immediate=immediate,

  File "/usr/lib/python2.7/site-packages/amqp/channel.py", line 1755, in _basic_publish
    if client_properties['capabilities']['connection.blocked']:

KeyError: u'connection.blocked'
```

## Solution

The most likely cause of this error is due to an older version of rabbitmq-server running on the system.
Try upgrading the version of rabbitmq to the latest version on epel and restart the iml-manager.target.

---

[Top](#job-scheudler-and-http-logs-show-keyerror-connectionblocked)
