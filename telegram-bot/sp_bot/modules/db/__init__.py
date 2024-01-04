from sp_bot import SESSION


class MongoOperations:
    'MongoDB operations'

    def __init__(self, SESSION):
        self.db = SESSION['spotipie']
        self.cursor1 = self.db['codes']
        self.cursor2 = self.db['users']

    def fetch_code(self, _id):
        'Fetches the code from the database'
        query = {'_id': _id}
        return self.cursor1.find_one(query)

    def delete_code(self, _id):
        'Deletes the code from the database'
        query = {'_id': _id}
        self.cursor1.delete_one(query)

    def fetch_user_data(self, telegram_id):
        'Fetches the user data from the database'
        query = {'tg_id': telegram_id}
        return self.cursor2.find_one(query)

    def update_user_username(self, telegram_id, new_username):
        'Updates user\'s username in the database'
        query = {'tg_id': telegram_id}
        newvalues = {"$set": {"username": new_username}}
        self.cursor2.update_one(query, newvalues)

    def delete_data(self, telegram_id):
        'Deletes the user data from the database'
        query = {'tg_id': telegram_id}
        self.cursor2.delete_one(query)

    def count_all(self):
        'Counts the total number of users in the database'
        return self.cursor2.find().count()

    def add_user(self, telegram_id, token):
        user = {
            "username": "User",
            "token": token,
            "isAdmin": False,
            "tg_id": telegram_id
        }
        self.cursor2.insert_one(user)


DATABASE = MongoOperations(SESSION)
