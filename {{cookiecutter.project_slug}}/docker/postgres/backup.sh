#!/bin/sh
# Take a base backup and keep the last 4 full ones
set -e
wal-g backup-push "$PGDATA"
wal-g delete retain FULL 4 --confirm
