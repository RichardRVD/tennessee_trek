from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User():
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.is_admin = data['is_admin']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.country = data['country']
        self.phone = data['phone']
        self.zip = data['zip']
        self.credit_card = data['credit_card']
        self.credit_card_type = data['credit_card_type']
        self.card_expiration = data['card_expiration']
        self.billing_address = data['billing_address']
        self.billing_city = data['billing_city']
        self.billing_state = data['billing_state']
        self.billing_country = data['billing_country']
        self.billing_zip = data['billing_zip']
        self.shipping_address = data['shipping_address']
        self.shipping_city = data['shipping_city']
        self.shipping_state = data['shipping_state']
        self.shipping_country = data['shipping_country']
        self.shipping_zip = data['shipping_zip']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users'
        results = connectToMySQL('tennessee_trekker_schema').query_db(query)

        users = []

        for row in results:
            users.append(User(row))
        return users

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('tennessee_trekker_schema').query_db(query, data)
    
        if result:
            return cls(result[0])


    @classmethod
    def register_new_user(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password, is_admin) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s, %(is_admin)s);'
        results = connectToMySQL('tennessee_trekker_schema').query_db(query, data)
        return results
    
    @classmethod
    def get_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL('tennessee_trekker_schema').query_db(query,data)
        users = []
        for row in result:
            users.append(User(row))
        return users

    @classmethod
    def is_admin(cls,data):
        query = 'SELECT * FROM users WHERE is_admin = 1;'
        result = connectToMySQL('tennessee_trekker_schema').query_db(query,data)
        admin = []
        for row in result:
            admin.append(User(row))
        return admin

    @staticmethod
    def valid_reg(data):
        is_valid=True

        if len(data['first_name'])< 2 or len(data['first_name']) > 45:
            flash('First name should be longer than 2 characters and less than 45 characters.','error_reg_first_name')
            is_valid=False

        if len(data['last_name']) < 2 or len(data['last_name']) > 45:
            flash('Last name should be longer than 2 characters and less than 45 characters.','error_reg_last_name')
            is_valid=False

        if not EMAIL_REGEX.match(data['email']):
            flash('Please enter a valid email address. Email should contain numbers or characters followed by the @ and a .com.','error_reg_email')
            is_valid=False

        if len(User.get_email(data)) != 0:
            flash('Email is already register. Please login or use a new email','error_reg_email')
            is_valid = False

        if len(data['password']) < 8:
            flash('Your password should be longer than 8 characters and less than 60 characters please.','error_reg_password')
            is_valid=False

        if data['password'] != data['confirm_password']:
            flash('Password and confirm passwords didnt match. Please check spelling and try again','error_reg_password')
            is_valid=False

        elif len(data['password']) > 60:
            flash('Your password should be longer than 8 characters and less than 60 characters please.','error_reg_password')
            print('e')
            is_valid=False

        elif data['password'] != data['confirm_password']:
            flash('Your passwords do not match. Please confirm your spell and try again.','error_reg_password')
            is_valid=False

        return is_valid
