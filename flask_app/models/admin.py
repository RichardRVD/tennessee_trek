from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Admin():
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def check_admin_by_email(cls):
        query = 'SELECT * FROM admins WHERE email = %(email)s;'
        result = connectToMySQL('tennessee_trekker_schema').query_db(query)

        admin = []
        for row in result:
            admin.append(Admin(row))
        return admin

    @classmethod
    def register_new_admin(cls,data):
        query = 'INSERT INTO admins (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);'
        results = connectToMySQL('tennessee_trekker_schema').query_db(query, data)
        return results

    @staticmethod
    def validate_reg(data):
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

        if len(Admin.check_admin_by_email(data)) != 0:
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