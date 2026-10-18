# Restore the database

This guide shows you how to restore the production database to its latest state or to a moment in the past. The restore goes into a new volume, so the current database stays untouched until you switch to the restored one.

## Before you begin

- Run all commands on the server, in the app directory (`~/<repository name>`).
- Find your Compose project name with `docker volume ls`. The examples use `myproject`, so the database volume is `myproject_postgres-data`.
- Times are in UTC.

## Restore into a new volume

1. Stop the app and the database, so no new writes are lost:

   ```bash
   docker compose stop backend postgres-backup postgres
   ```

2. Create an empty volume:

   ```bash
   docker volume create myproject_postgres-data-restored
   ```

3. Restore into it:

   - **If you want the latest state,** run the restore without a time:

     ```bash
     docker compose run --rm --no-deps -v myproject_postgres-data-restored:/restore \
       postgres-backup restore.sh
     ```

   - **If you want a moment in the past,** pass the time. Relative times such as `"10 minutes ago"` also work.

     ```bash
     docker compose run --rm --no-deps -v myproject_postgres-data-restored:/restore \
       postgres-backup restore.sh "2026-10-02 14:25"
     ```

   The output ends with a `restored_up_to` timestamp. Check that it's the moment you expect.

## Switch to the restored volume

1. Create or edit `docker-compose.override.yml` and point the database volume at the restored one:

   ```yaml
   volumes:
     postgres-data:
       name: myproject_postgres-data-restored
       external: true
   ```

2. Start the stack and take a fresh backup:

   ```bash
   docker compose up -d
   docker compose exec postgres-backup backup.sh
   ```

3. Check the site. When everything looks right, remove the old volume:

   ```bash
   docker volume rm myproject_postgres-data
   ```

## Troubleshooting

`/restore is not empty`
: The target volume already contains data. Create a new, empty volume and restore into that.

`Stop the database first`
: The database is still running. Run the `docker compose stop` command from step 1 of the restore.
