# About backups

A generated project backs up PostgreSQL with [WAL-G](https://github.com/wal-g/wal-g), which combines full backups with a continuous log of changes. Together, they let you restore the database to any moment, not only to the last nightly backup.

## How it works

PostgreSQL writes every change to its write-ahead log (WAL) before it applies it. The project configures PostgreSQL to hand each finished WAL segment to WAL-G, and to finish a segment at least once a minute even when traffic is low.

Base backup
: A full copy of the database. The `postgres-backup` container takes one on its first start and then every night at 03:00 UTC. It keeps the last 4.

WAL archive
: Every change since the oldest kept base backup, in order.

To restore, WAL-G fetches the newest base backup taken before the target time. PostgreSQL then replays the archived WAL on top of it and stops at the exact moment you asked for.

## What you can lose

Up to about a minute of changes, the time a WAL segment can wait before it's archived. The restore script also copies WAL that the old server hadn't archived yet, so in a planned restore on a working server you usually lose nothing.

## Why not `pg_dump`

A nightly `pg_dump` is simpler, but it can lose a whole day of data, and restoring a large dump is slow. Point-in-time recovery also covers the most common real disaster, which is a bad migration or a mistaken `DELETE`, not a dead disk. You restore to the minute before the mistake.

## Where backups live

By default, backups go to the `postgres-backups` Docker volume on the same server. That protects against mistakes, but not against losing the server. For real protection, store them off the server, as in {doc}`../how-to/store-backups-in-s3`. With S3, backups are encrypted with libsodium before they leave the server, so the storage provider can't read them.

## Related

- {doc}`../how-to/restore-the-database`
- {doc}`../reference/environment`
