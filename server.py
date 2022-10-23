from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import admins
from flask_app.controllers import trips
from flask_app import static


if __name__=='__main__':
    app.run(debug=True, port=5001)