<a name="top"></a>
[Support Table of Contents](TOC.md)

# Common Troubleshooting And Tips

## How do I get a collection of logs on a node?

```
# iml-diagnostics
```

## How do I restart a specific chroma service (such as the view server) on the manager node in production?

```
# supervisorctl -c /usr/share/chroma-manager/production_supervisord.conf restart <service_name>
// eg. # supervisorctl -c /usr/share/chroma-manager/production_supervisord.conf restart view_server
```

## How do I run a django South database migration?

```
[/usr/share/chorma-manager] #./manage.py schemamigration chroma_core —auto
```

Note that `chroma_core` is the app name.

## How do I remove a newer module installed with yum and replace it with a previous version?

```
rpm -Uvh --oldpackage <path-to-rpm-file>
```

## How do I get metric data from the database?

```
# su - postgres -c "psql -d chroma -c 'select * from chroma_core_sample_10 order by dt desc limit 20;'"
# su - postgres -c "psql -d chroma -c 'select * from chroma_core_sample_60 order by dt desc limit 20;'"
# su - postgres -c "psql -d chroma -c 'select * from chroma_core_sample_300 order by dt desc limit 20;'"
# su - postgres -c "psql -d chroma -c 'select * from chroma_core_sample_3600 order by dt desc limit 20;'"
# su - postgres -c "psql -d chroma -c 'select * from chroma_core_sample_86400 order by dt desc limit 20;'"
```

## How do I put the chroma-agent into debug mode?

```bash
systemctl kill -s SIGUSR2 chroma-agent.service
```

## How do I backup the chroma-database?

```
# su - postgres -c "pg_dump -U chroma chroma > /tmp/db_backup_xxx.sql"
```

## How do I backup the chroma-database WITHOUT metric data?

**Note** This is very helpful if you don't need the metric data and the database that is being exported is very large.

```
# su - postgres -c "pg_dump -U chroma -F p -w -T 'chroma_core_series*' -T 'chroma_core_sample*' -T 'chroma_core_logmessage*' -f /tmp/chromadb_backup_xxx.sql"
```

## How do I import a backed up database?

```
# su - postgres -c "dropdb chroma; createdb chroma; psql chroma < /tmp/db_backup_xxx.sql"
```

## How do I interact with the device scanner?

To interact with the device-scanner in real time the following command can be used to keep the stream open such that updates can be seen as the data changes:

```
cat - | ncat -U /var/run/device-scanner.sock | jq
```

If interaction is not required, device info can be retrieved from the device-scanner by running the following command:

```
echo "{\"ACTION\": \"info\"}" | ncat -U /var/run/device-scanner.sock | jq
```

Alternatively, the following command will retrieve device data from the device-scanner as well:

```
echo '"Info"' | socat - UNIX-CONNECT:/var/run/device-scanner.sock | jq
```

## What do I do if node is crashing with a segfault?

This could be caused by a number of things:

1. A dependency that was installed with node gyp may need to be re-installed properly
2. The installed version of node could be blowing up. Try to trace through the service in question and identify where the crash is. For example, if you see the crash happen during an http request, try bringing up a node REPL and making a quick http request. For example:

   ```bash
   [root@somenode]# node
   > var http = require('http');
   undefined
   > http.get('google.com')
   { domain: null,
     _events: { socket: { [Function: g] listener: [Function] } },
     _maxListeners: 10,
     output: [ 'GET google.com HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\n\r\n' ],
     outputEncodings: [ undefined ],
     writable: true,
     _last: true,
     chunkedEncoding: false,
     shouldKeepAlive: true,
     useChunkedEncodingByDefault: false,
     sendDate: false,
     _headerSent: true,
     _header: 'GET google.com HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\n\r\n',
     _hasBody: true,
     _trailer: '',
     finished: true,
     _hangupClose: false,
     socket: null,
     connection: null,
     agent:
     { domain: null,
       _events: { free: [Function] },
       _maxListeners: 10,
       options: {},
       requests: {},
       sockets: { 'localhost:80': [Object] },
       maxSockets: 5,
       createConnection: [Function] },
     socketPath: undefined,
     method: 'GET',
     path: 'google.com',
     _headers: { host: 'localhost' },
     _headerNames: { host: 'Host' } }
   > Segmentation fault
   ```

If it turns out that the installed version of node is indeed causing the segfault then there is probably an issue with the bundled version. Start by uninstalling the version of node that is installed:

```bash
yum list installed | grep nodejs
```

> nodejs-0.10.36-3.el7.x86_64

```bash
rpm -e --nodeps "nodejs-0.10.36-3.el7.x86_64"
```

After installing nodejs, download the appropriate rpm; Check this location for reference: [https://rpm.nodesource.com/pub_0.10/el/7/x86_64/](https://rpm.nodesource.com/pub_0.10/el/7/x86_64/). Now, use yum to install nodejs using the rpm:

```bash
yum install nodejs-0.10.36-1nodesource.el7.centos.x86_64.rpm
```

Restart the manager services after the installation completes:

```bash
chroma-config restart
```

Connect to the GUI and use the web app to ensure everything is working correctly.

[top](#top)
