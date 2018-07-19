# DatabaseError: current transaction is aborted, commands ignored until end of transaction block

[Support Table of Contents](TOC.md)

## Overview

If the following error occurrs when loading the IML page:

> DatabaseError: current transaction is aborted, commands ignored until end of transaction block

This means that a transaction did not complete successfully and can occur in instances such as a power failure while a transaction is being written. 

## Rolling back the transaction

Since the transaction did not complete, the first thing that needs to be done is to roll back the aborted transaction. This can be done on using the postgres repel:

```bash
cd /usr/share/chroma-manager
python manage.py dbshell
chroma=> rollback;
```

After rolling back the transaction, attempt to load the IML GUI again. It's possible that a new error will appear:

> DatabaseError: could not find left sibling of block 35383 in index 

More than likely, this means that an index has become corrupt. One option is to attempt to fix / clean the corrupt index, but this may be more trouble than it is worth. A more direct solution is to export the database along with the db bits, drop the database, create the database, and then import the backup. This process is straight forward and works well. To backup the database, select one of the commands below. Note that backing up without metrics will produce a much smaller database file, but either option will work:

```bash
# Backup with metric data
su - postgres -c "pg_dump -U chroma chroma > /tmp/chromadb_backup_full.sql"

# Backup without metric data
su - postgres -c "pg_dump -U chroma -F p -w -T 'chroma_core_series*' -T 'chroma_core_sample*' -T 'chroma_core_logmessage*' -f /tmp/chromadb_backup_without_metrics.sql"
```

Now that the database is backed up in the /tmp directory, use the following script to drop the current database, create a new one, and import the backup: [import customer database](scripts/import-customer-database.md). Once the database has been restored and IML loads, attempt to load the IML GUI. It should now load without any issues.

---

[Top](#databaseerror-current-transaction-is-aborted-commands-ignored-until-end-of-transaction-block)