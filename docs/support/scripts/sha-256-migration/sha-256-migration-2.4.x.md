# Sha 256 Migration for IML@2.4.x

[Support Table of Contents](../../TOC.md)

The sha-256 migration script is a tool used to migrate old certificates that were created with a sha-1 encryption to sha-256 encryption. This set of scripts is designed to be run on an IML manager node running 2.4.x. It will locate all MDS and OSS nodes registered with the manager and update their certificates accordingly.

* [agent.py](2.4.x/agent.py)
* [chroma_manager_crypto.py](2.4.x/chroma_manager_crypto.py)
* [crypto.py](2.4.x/crypto.py)
* [main](2.4.x/main)
* [manager.py](2.4.x/manager.py)
* [README.md](2.4.x/README.md)
* [views.py](2.4.x/views.py)

Packaged Archive: