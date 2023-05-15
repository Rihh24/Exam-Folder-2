from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user

class Tree:
    db = "arbortrary"
    def __init__(self, data):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.date_planted = data['date_planted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
    
    @classmethod
    def get_all_trees(cls):
        query = "SELECT * FROM trees JOIN users on trees.user_id = users.id;"
        results = connectToMySQL('arbortrary').query_db(query)
        trees = []
        for row in results:
            this_tree = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_tree.creator = user.User(user_data)
            trees.append(this_tree)
        return trees

    @classmethod
    def get_user_trees(cls):
        query = "SELECT * FROM trees JOIN users on trees.user_id = users.id WHERE user_id = %(id)s;"
        results = connectToMySQL('arbortrary').query_db(query)
        trees = []
        for row in results:
            this_tree = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_tree.creator = user.User(user_data)
            trees.append(this_tree)
        return trees
    

    @classmethod
    def save_tree(cls, data):
        query = "INSERT INTO trees(species,location,reason,date_planted, created_at, updated_at, user_id) VALUES(%(species)s, %(location)s,%(reason)s,%(date_planted)s,NOW(),NOW(),%(user_id)s);"
        result = connectToMySQL('arbortrary').query_db(query,data)
        return result

    @classmethod
    def get_one_tree(cls, data):
        query = "SELECT * FROM trees WHERE trees.id = %(id)s;"
        trees_from_db = connectToMySQL('arbortrary').query_db(query, data)
        return cls(trees_from_db[0])
    
    @classmethod
    def get_tree_id(cls,data):
        query = "SELECT * FROM trees JOIN users on trees.user_id = users.id WHERE trees.id = %(id)s;"
        result = connectToMySQL('arbortrary').query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_tree = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_tree.creator = user.User(user_data)
        return this_tree

    @classmethod
    def update_tree(cls, data):
        query = "UPDATE trees SET species=%(species)s,location=%(location)s,reason=%(reason)s, date_planted=%(date_planted)s WHERE id = %(id)s;"
        result= connectToMySQL('arbortrary').query_db(query,data)
        return result
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM trees WHERE id = %(id)s;"
        return connectToMySQL('arbortrary').query_db(query,data)
    

    @staticmethod
    def validate_new_tree(data):
        is_valid = True
        if len(data['species']) < 3:
            flash("Species Name must be more than 3 Characters.")
            is_valid = False
        if len(data['location']) < 2:
            flash("Location must be more than 2 characters.")
            is_valid = False
        if len(data['reason']) > 50:
            flash("Reason must be less than 50 characters")
            is_valid = False
        if data['date_planted'] == '':
            flash("Please input a date.")
            is_valid = False
        return is_valid
