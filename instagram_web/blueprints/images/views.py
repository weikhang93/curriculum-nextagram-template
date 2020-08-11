from flask import redirect, render_template , url_for , Blueprint , request , flash
from models.images import Images
from models.user import User
from flask_login import login_required, current_user
from werkzeug import secure_filename
from instagram_web.util.helpers import upload_file_s3



images_blueprint=Blueprint('images',
                            __name__,
                            template_folder="templates")





@images_blueprint.route('/new', methods=["GET"])
def new():
    return render_template("images/new.html")




@images_blueprint.route("/", methods=["POST"])
@login_required
def create():
    user=User.get_or_none(User.id==current_user.id)

    #This is to make sure a file is submitted, or to prevent prople from submitting empty form.
    if "images" not in request.files:
        flash("No file provided", "danger")
        return redirect(url_for('images.new'))

    #file is an instance of a File Class. 
    file= request.files.get('images')

    file.filename=secure_filename(file.filename)

    #upload_file_s3 from util.helpers.py takes in 2 arguement
    #1st arguement is the file object itself, the second arguement
    #is the foldername. Which is the username in our case.
    image_path=upload_file_s3(file , user.username)

    image= Images(user=user, image_url=image_path)

    if image.save():
        flash("Image uploaded", "primary")
        return redirect(url_for('users.show' , username=current_user.username))
    else:
        flash("Try again bruh, something went wrong" , "danger")
        return render_template("images/new.html")


    
    
    
    


    

