# SHA-256 Browser Migration

[Sha 256 Migration for IML@2.4.x](../sha-256-migration-2.4.x.md)

This repo serves as an automated way to update
existing installations to use SNI + SHA-256 certificates.

Chrome is sunsetting SHA-1 support (which our certs have been signed with).


## How to use

1. Back up your existing httpd confs.
2. Put this repo on your manager node running IEEL 2.4.x.
3. cd into this repo.
4. run `./main`.

At this point, your system should now be served using a sha256 certificate.
