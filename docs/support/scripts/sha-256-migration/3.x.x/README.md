# SHA-256 Browser Migration

[Sha 256 Migration for IML@3.x.x](../sha-256-migration-3.x.x.md)

This repo serves as an automated way to update
existing installations to use SHA-256 certificates.

Chrome is sunsetting SHA-1 support (which our certs have been signed with).
https://security.googleblog.com/2014/09/gradually-sunsetting-sha-1.html


## How to use

1. Put this repo on your manager node running IEEL 3.x.x
2. cd into this repo.
3. run `./main`.

At this point, your system should now be served using a sha256 certificate.
