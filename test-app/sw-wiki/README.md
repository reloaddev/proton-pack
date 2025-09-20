# Star Wars Wiki
Learn everything about Star Wars. 

## Purpose
This is a test app to test the Proton Pack, a database migration safety analyzer. The app
connects to a postgres database, that includes different tables containing Star Wars data.
You can use the app to create database migrations / schema changes, which you can analyze
with the Proton Pack. Once your analysis is done, you can use this app to apply the migration
in a controlled environment.

## Manual setup
Assuming that you are in the outer `sw-wiki` directory.
1. Create a venv in the root of the project, `python3 -m venv .venv`
2. Install the requirements, `pip install -r requirements.txt`
3. Run the app `flask --app sw_wiki run --debug`

## Automatic setup
The sw-wiki test app can be deployed using make. Check the README.md of test-app.

## Run Migrations
- (One time only) Run `flask --app sw_wiki db init` to create a migration repository.
- Run `flask --app sw_wiki db migrate -m "Migration message"` to generate a migration.
- Run `flask --app sw_wiki db upgrade` to apply the migration. This will most likely change your database schema.