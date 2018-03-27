# Sha 256 Migration for IML@3.x.x

[Support Table of Contents](../../TOC.md)

The sha-256 migration script is a tool used to migrate old certificates that were created with a sha-1 encryption to sha-256 encryption. This set of scripts is designed to be run on an IML manager node running 3.x.x. It will locate all MDS and OSS nodes registered with the manager and update their certificates accordingly.

* [agent.py](3.x.x/agent.py)
* [chroma_manager_crypto.py](3.x.x/chroma_manager_crypto.py)
* [crypto.py](3.x.x/crypto.py)
* [main](3.x.x/main)
* [manager.py](3.x.x/manager.py)
* [README.md](3.x.x/README.md)

Packaged Archive: [sha-256-migration-3.x.x](https://github.com/intel-hpdd/Support/releases/download/v0.0.2/sha-256-migration-3.x.x.tar)
