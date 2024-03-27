from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import config
from models import User

app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug = config.DEBUG
app.config.from_object(config)
CORS(app)

login_manager = LoginManager(app)
login_manager.init_app(app)

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


from views import *

if __name__ == '__main__':

    app.run()
