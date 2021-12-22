db.createUser(
    {
        user: 'admin',
        pwd: 'SuperSecret',
        roles: [
            {
                role: 'readWrite',
                db: 'ts_config'
            },
            {
                role: 'readWrite',
                db: 'admin'
            }
        ],
    }
);

db.auth('admin', 'SuperSecret')

db = db.getSiblingDB('ts_config')

db.createCollection('config');

db.config.insertMany([
    {
        "exportingDataController": "https://exportingDataController.tld",
        "importingDataController": "https://importingDataController.tld",
        "config": {
            "test": "test"
        },
        "createdAt": "2021-08-05T16:29:17.406Z",
        "updatedAt": "2021-08-05T16:29:17.406Z",
    },
]);
