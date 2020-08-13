from flask import Blueprint, render_template , request,redirect , url_for , flash, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user , login_required , logout_user
from instagram_web.util.google_oauth import oauth



sessions_blueprint=Blueprint('sessions',
                                __name__,
                                template_folder='templates')



@sessions_blueprint.route('/new' , methods=['GET'])
def new():
    return render_template('sessions/new.html')



@sessions_blueprint.route('/delete' , methods=['POST'])
@login_required
def destroy():
    # session.pop('user_id', None)
    logout_user() #deleting the session
    flash("GOODBYE MY LOVE")
    return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/google_login')
def google_login():
    # url_for will return a strings. 
    # _external=True is to make google to direct back to our view
    #function , without _external=True, the redirect_uri will only be
    # sessions.authorize in stead of localhost:50000/sessions.authorize

    redirect_uri= url_for('sessions.authorize' , _external=True)

    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google')
def authorize():
    oauth.google.authorize_access_token()
    email=oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    
    user=User.get_or_none(User.email==email)
    if user:
        flash("Succesfully logged in" , "primary")
        login_user(user)
        return redirect(url_for('users.show' , username=user.username))

    else:
        flash("EITHER U HAVE NO GOOGLE ACCOUNT OR YOU DON'T HAVE NEXTAGRAM ACCOUNT..... but either way... PLEASE FUCK OFF LA", "danger")
        return redirect(url_for('sessions.new'))



    


@sessions_blueprint.route('/', methods=['POST'])
def create():
    email=request.form.get("email")
    password=request.form.get("password")
    
    # below method is not efficient
    # for user in users_list:
    #     if user.email==email:
    #         if check_password_hash(user.password,password):
    #             print("Succesfully log in / session created")
    #             return "Succesfully log in"

    #         else:
    #             print("wrong password bruh")
    #             return "Wrong password bitch"
    user=User.get_or_none(email=email)
    if user:
        if check_password_hash(user.hashed_password,password):
            flash("SUCCESFULLY LOGIN MOTHERFUCKER" , "primary")
            # session['user_id']=user.id
            login_user(user)
            return redirect(url_for('users.show' , username=user.username ))
        else:
            flash("Wrong password bitch" , "danger")
            return redirect(url_for('sessions.new'))
    else:
        flash("NO SUCH USERNAME LA BRUH" , "danger")
        return redirect(url_for('sessions.new'))