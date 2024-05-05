# Script to load the test database into the MongoDB instance

mongoimport --jsonArray \
    --db test-data \
    --collection app.blueprints.drift \
    --file tmp/database/test-drifts.json

mongoimport --jsonArray \
    --db test-data \
    --collection app.blueprints.user \
    --file tmp/database/test-users.json
