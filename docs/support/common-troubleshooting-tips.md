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
```
touch /tmp/chroma-agent-debug
kill -s SIGUSR2 <chroma-agent-pid>

# or in IML 4.1

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

[top](#top)
