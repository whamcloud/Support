<a name="top"></a>
[Support Table of Contents](../TOC.md)

## Loading a customer's database

The following script will load a customers database into a new installation of IML. 

### Usage:
```
./import_database.py /path/to/database/file.sql
```

### Script:
```python
#! /usr/bin/python

import sys, os
import subprocess
import string
import psycopg2
from functools import partial

sys.path.append('/usr/share/chroma-manager')
from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.conf import settings

from chroma_core.lib.util import CommandLine
cl = CommandLine()
try_shell = cl.try_shell

other_db_bits_file = '/tmp/other-db-bits.sql'

try:
    databasefile = sys.argv[1]
    print "Importing %s" % databasefile
except Exception as e:
    print "import_database: missing database file location.\n"
    print "Usage: './import_database <database-file-location.sql>'"

def psql_command (cmd):
    try_shell(['su', '-', 'postgres', '-c'] + cmd)

def drop_chroma_db ():
    try:
        print "Dropping chroma db."
        psql_command(['dropdb chroma'])
    except Exception as e:
        print "Error dropping the database."

def create_chroma_db ():
    try:
        print "Creating chroma db."
        psql_command(['createdb chroma'])
    except Exception as e:
        print "Error creating the database."

def write_db_other_bits (db_bits_file):
    try:
        print "Writing other db bits."
        psql_command(["pg_dump -U chroma -F p -w -f %s -t 'chroma_core_series*' -t 'chroma_core_sample_*' -t 'chroma_core_logmessage*'" % db_bits_file])
    except Exception as e:
        print "Error exporting other db bits."

def import_chroma_db (db_file):
    try:
        print "Importing Database."
        psql_command(['psql chroma -f %s' % db_file])
    except Exception as e:
        print "Error importing database."

def import_other_db_bits (db_bits_file):
    try:
        print "Importing other db bits."
        psql_command(['psql chroma -f %s' % db_bits_file])
    except Exception as e:
        print "Error importing other db bits."

def import_database (db_file):
    try:
        print "Stopping chroma manager."
        try_shell (['chroma-config', 'stop'])
        
        write_db_other_bits(other_db_bits_file)
        drop_chroma_db ()
        create_chroma_db ()
        import_chroma_db (db_file)
        import_other_db_bits (other_db_bits_file)

        print "starting chroma manager"
        rc, out, err = try_shell (['chroma-config', 'start'])
        print "Result: \nStdout: %s\nStderr: %s" % (out, err)

    except Exception as e:
        print e

import_database (databasefile)
```

[top](#top)