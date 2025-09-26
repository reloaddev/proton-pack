# Ghostbusters Wiki
Learn everything about the Ghostbusters. 

## Purpose
This is a test app to test the Proton Pack, a database migration safety analyzer. The app
connects to a postgres database, that includes different tables containing Ghostbusters data.
You can use the app to create database migrations / schema changes, which you can analyze
with the Proton Pack. Once your analysis is done, you can use this app to apply the migration
in a controlled environment.

## Manual setup
Assuming that you are in the outer `ghostbusters-wiki` directory.
1. Create a venv in the root of the project, `python3 -m venv .venv`
2. Install the requirements, `pip install -r requirements.txt`
3. Run the app `flask --app ghostbusters_wiki run --debug`

## Automatic setup
The ghostbusters-wiki test app can be deployed using make. Check the README.md of test-app.

## Run Migrations
- (One time only) Run `flask --app ghostbusters_wiki db init` to create a migration repository.
- Run `flask --app ghostbusters_wiki db migrate -m "Migration message"` to generate a migration.
- Run `flask --app ghostbusters_wiki db upgrade` to apply the migration. This will most likely change your database schema.
Often times, running a migration will also include some type of seeding, meaning that the migration will also insert data into the database.

## Generate SQL version of migrations
Flask-Migrate migrations are typically python files. They are converted behind the scenes by a library
called Alembic. If you want, for any reason, see the SQL version of a migration, you can generate by 
using the following commands. Just use the `<version-no>` from the Python migration file, that you want to
transform into SQL.
```
## Step into application directory
cd ghostbusters-wiki

## Create SQL version of Flask-Migrate migration
flask --app ghostbusters_wiki db upgrade <version-no> --sql > migrations/sql/<version-no>.sql
```