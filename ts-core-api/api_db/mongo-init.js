db.createUser(
    {
        user: 'admin',
        pwd: 'SuperSecret',
        roles: [
            {
                role: 'readWrite',
                db: 'ts_api'
            },
            {
                role: 'readWrite',
                db: 'admin'
            }
        ],
    }
);

db.auth('admin', 'SuperSecret')

db = db.getSiblingDB('ts_api')

db.createCollection('data_disclosed');
db.createCollection('transfer_job');

db.data_disclosed.insertMany([
    {
        "user_id": "12345",
        "dataDisclosed": {
            "name": "John",
            "age": "25",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "12345",
            "phone": "123-456-7890"
        },
        "createdAt": "2021-08-05T16:29:17.406Z",
        "updatedAt": "2021-08-05T16:29:17.406Z"
    }
]);