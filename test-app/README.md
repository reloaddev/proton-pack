# Test App to test Proton Pack
This test app is used to test the Proton Pack. It includes a Flask application and a postgres
database, which you can both deploy using make. Running the make command, will spin up the
application and database using docker-compose.

## Usage
### Starting and stopping the app
You can start both the application and the database using make.

Assuming that you are in the `test-app` directory.
- To run the test app, run `make up`.
- To stop the test app, run `make down`.
- To clean up the test app, run `make reset`. (This will reset the data stored in the database)

### Connecting to the database
- To connect to psql, run `make psql`.



