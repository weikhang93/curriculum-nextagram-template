from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import re
from playhouse.hybrid import hybrid_property


#UserMixin for flask-login thingy to enable usag of current_user.authenticated... etc
class User(UserMixin,BaseModel):
    username = pw.CharField(unique=True , null=False)
    email=pw.CharField(unique=True, null=False)
    hashed_password=pw.CharField(null=False)
    password=None
    image_path=pw.TextField(null=True)
    is_private=pw.BooleanField(default=True)
    

    @hybrid_property
    def full_image_path(self):
        if self.image_path:
            from app import app
            return app.config.get('S3_LOCATION')+self.image_path

        else:
            return ""
            




    def validate(self):
        existing_user_email=User.get_or_none(User.email==self.email)
        
        ## the 2nd part of the if statement below ( and existing_user_email.id !=self.id) , is added to
        ##allowed user to keep their email when updating other criteria. same goes for username
        if existing_user_email and existing_user_email.id != self.id:
            # flash("Sorry man this email has already taken" , 'danger')
            self.errors.append(f"User with {self.email} already exist!")

        existing_user_username=User.get_or_none(User.username==self.username)

        if existing_user_username and existing_user_username.id != self.id:
            # flash ("Sorry man this username has already used" , 'danger')
            self.errors.append(f"User with {self.username} already exists!")


        ##IF self.password is added during update part to enable user to keep their old password and only update other 
        ##credential, otherwise,self.password will be an None. to make sure that its None when user key-ed in nothing,
        ## We have to to some conditinoing on our views.py update view fuction,otherwise if we just use 
        ##password=request.form.get('password'), even if user key'ed in nothing, the form will return an "" empty string.
        if self.password:
            if len(self.password)<=5:
                self.errors.append(f"Please input more than 6 characters")


            has_lower = re.search(r"[a-z]", self.password)
            has_upper = re.search(r"[A-Z]", self.password)
            has_special = re.search(r"[\[ \] \* \$ \% \^ \& \# \! \@]", self.password)

            if not has_lower:
                self.errors.append("Password must contain at least 1 lowercase alphabets")

            if not has_upper:
                self.errors.append("Password must contain at least 1 UPPER case alphabets")
            if not has_special:
                self.errors.append("Password must contain at least 1 special character !@#$%$^")
            
            if has_lower and has_upper and has_special:
                self.hashed_password=generate_password_hash(self.password)

        








        # self.hashed_password=generate_password_hash(self.password)

    




    
