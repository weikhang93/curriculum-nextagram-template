import os
import config
from flask import Flask
from models.base_model import db
from flask_login import LoginManager
from models.user import User

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

# csrf and init
# __init__py is used when we are trying to import a package, the __init__py 
#file will be executed , usually its empty, but i dono why do we have to have 
#all those codes there, and i also don't know where do we actually import this 
#package. Because there seems to be no other .py file on the same directory as
#these __init__py inside instagram_web/instagram_api.





app = Flask('NEXTAGRAM', root_path=web_dir)


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

login_manager = LoginManager()  
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) # get id from session,then retrieve user object from database with peewee query

login_manager.login_view = "sessions.new" 
login_manager.login_message = "Please log in before proceeding"
login_manager.login_message_category = "warning"

@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
