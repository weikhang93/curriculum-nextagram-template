from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from instagram_web.util.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)


# I still don't know where does our app inject/use jinja, but the thing that i got away is that....i should probably google how to use jinja loop control in flask
# As of how to use other extension next time... its basically that 1 line below this comment. so just change the extension name i guess. The gist from this is probably to know that we want to edit our jinja Environment by adding another extension. Which in this case its jinja2.ext.loopcontrols.
# The 2 line that is not being used is when jingwen try and error to help me with my needs, which is to use the break function in my html. but when i tried to write my gist/documentation, it felt kinda redundant... therefore i tried to comment it out and test is the break function still works. and... ya... it works. SO in conclusion i only need to understand that i will have to add the extension inside the jinja enviroment and this updated enviroment has to be included inside my app.

# import jinja2
# jinja_env = jinja2.Environment(extensions=['jinja2.ext.loopcontrols'])
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/images/<image_id>/donations" )

# ALL these "general rule" below is just because of RESTFUL convention, our app should still work if we ignore them, but its a better practice to let other developer to know wtf are we doing.


# first thing first, if i see a nested prefix, that imply there is a certain relationship between images and donations, but it doesn't tell us what type of relationship it is. One/both of it will have a foreignkeyfield , in this case its on donations.
# for donations, because of the fact that i want to know which image_id am i donating to, then i should probably realise that this route will require an image_id, which will end up being a nested route.

# for images, altho there is a foreignkeyfield in image model/table, but because i know i only add image to current_user, hence there is no need of nested route.



@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')
