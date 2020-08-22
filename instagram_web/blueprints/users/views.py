from flask import Blueprint, render_template , request,redirect , url_for , flash
from models.user import User
from werkzeug.security import generate_password_hash
from flask_login import login_required,current_user
from instagram_web.util.helpers import upload_file_s3
from werkzeug import secure_filename
from models.fanidol import FanIdol
users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username=request.form.get('username')
    password=(request.form.get('password'))
    email=request.form.get('email')

    new_user=User(username=username,password=password,email=email)

    if new_user.save():   
        print("Succesfully added into db")
        return redirect(url_for('users.index'))
    else:
        for error in new_user.errors:
            flash(error)

        return render_template('users/new.html', username=username, email=email)


@users_blueprint.route('/<username>', methods=["GET"])

#some view function takes in id, some takes in username, actually if we were to use id for all of them, it
#still gonna work, its just that from a client/user perspectives, they are not gonna remember their id or might not 
#even know their id , which is why we use username as the arguements. 
#Another thing to remember is that if we want to use username, we have to make sure the username Unique=True at our User model
def show(username):
    print(__name__)
    x=1
    y=0
    user=User.get_or_none(User.username==username)
    for fanidolrow in current_user.idol:
        if fanidolrow.idol.id==user.id:
            x=0
            if fanidolrow.is_approved==True:
                y=1
            break
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(x)

    return render_template("/users/show.html", user=user,x=x , y=y)


@users_blueprint.route('/', methods=["GET"])
@login_required
def index():
    users=User.select()
    return render_template('users/index.html' , users=users)


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    return render_template('/users/edit.html')




@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user_to_update=User.get(User.id==id)
    username=request.form.get('username')
    email=request.form.get('email')
    password=request.form.get('password')

    user_to_update.username=username
    user_to_update.email=email
    #This is the part to make the password back to default which is None in our users.py
    if len(password)!=0:
        user_to_update.password=password

    if user_to_update.save():
        flash("Your profile's detail has been updated")
        return redirect(url_for('home'))
    else:
        flash('Failed to update')
        for error in user_to_update.errors:
            flash(error)
        return redirect(url_for('users.edit',id=current_user.id))




@users_blueprint.route('/<id>/upload_profile_image' , methods=["POST"])
@login_required
def upload_profile_image(id):
    user=User.get_or_none(User.id==id) ## to make sure someone can't manually key in users/234234234/upload_profile_image
    if user:
        if current_user.id==user.id: ## to prevent user1 to upload image for user2
            
            #This is to make sure a file is submitted, or to prevent people from submitting empty form.
            if "profile_image" not in  request.files:
                flash("No file provided")
                return render_template('users/edit.html')

            #File is a special type of data to be passed in, we can't use request.form.get to get a file.
            file=request.files.get("profile_image") ## This is equivalent to file=request.file["profile_image"]
            
            #At Line 96, file.filename is whatever filename that we put in including the extension.
            #Eg. if we choose shoe.jpg, then the file.filename would be "shoe.jpg"

            #line 102 just convert it to some more secured name, Eg. if the filename is sth weird like
            #  @#$%1241@#$@$!@#!#$.jpeg , it could break our app. secure_filename is a function from werkzeug to convert
            #the @#$%1241@#$@$!@#!#$.jpeg into secured version of it.
            file.filename=secure_filename(file.filename)

            image_path=upload_file_s3(file,user.username)

            user.image_path=image_path
            if user.save():
                flash("Succesfully uploaded your new Profile Imagee")
                return redirect(url_for('users.show' ,username=user.username))
            else:
                flash("Failed to upload your Profile Image bruh, probably because you're a potato")

        else:
            flash("Don't even think about it you mofos")
            return redirect(url_for('users.show' ,username=user.id))

    else:
        flash("NO SUCH USER! DON'T try to be cute please")
        return redirect(url_for('home'))

# @users_blueprint.route('/follow/<id>')
# def follow(id):
#     user=User.get_by_id(id)

#     user.is_private=False
#     user.save()
#     return "hehehe"

@users_blueprint.route('/private' , methods=["POST"])
def private():
    ticks=request.form.get("is_private")
    user=User.get_or_none(User.id== current_user.id)

    if ticks=="Ticked":
        user.is_private=True
        user.save()
        flash("Your profile is now private!" , "primary")
        return redirect(url_for('users.show' , username=current_user.username))
    else:
        user.is_private=False
        user.save()
        flash("Your profile is now public" , "primary")
        return redirect(url_for('users.show' , username=current_user.username))

    
    

# We hav to put <id> as our route params because we want to know which user to follow
# in our view function later, without the params, the view function will have no access
# to the id that is passed down from the url_for.
# and the reason we put <id> infront of /follow instead of /follow/<id> is because of
#Restful convention. cause even if we put /follow/<id> we should also be able to interpret it.
@users_blueprint.route('<id>/follow/' , methods=["POST"])
def follow(id):
    for fanidolrow in current_user.idol:
        print(type(fanidolrow.idol))
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(type(fanidolrow.idol_id))
        print(type(current_user))
        print(User)


    fanidol=FanIdol(fan=current_user.id, idol=id)

    fanidol.save()


    
    

    return "LALALA"





@users_blueprint.route('/unfollow' , methods=["POST"])
def unfollow():
    pass



        



