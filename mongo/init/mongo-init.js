db.createUser(
    {
        user: 'vv8',
        pwd: 'vv8',
        roles: [
            {
                role: "root",
                db: 'vv8'
            }
        ]
    }
);