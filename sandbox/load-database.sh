# Script to load the test database into the MongoDB instance

mongoimport --jsonArray \
    --db test-data \
    --collection app.experiments \
    --file tmp/database/test-experiments.json

mongoimport --jsonArray \
    --db test-data \
    --collection app.blueprints.user \
    --file tmp/database/test-users.json

mongoimport --jsonArray \
    --db test-data \
    --collection app.00000000-0000-0001-0001-000000000001 \
    --file tmp/database/test-01-drifts.json

mongoimport --jsonArray \
    --db test-data \
    --collection app.00000000-0000-0001-0001-000000000002 \
    --file tmp/database/test-02-drifts.json

mongoimport --jsonArray \
    --db test-data \
    --collection app.00000000-0000-0001-0001-000000000003 \
    --file tmp/database/test-03-drifts.json

mongoimport --jsonArray \
    --db test-data \
    --collection app.00000000-0000-0001-0001-000000000004 \
    --file tmp/database/test-04-drifts.json
