import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property





# image.user.username  when we have an image instance named image, we can access the owner of it by using image.user.name
# or image.user.id

# user.images  if we have an User instance named user, we can access the whole list of images that the user have.
    
class Images(BaseModel):
    #i should add a constraint on user attributes. which is 
    # on_delete="Cascade" so that the app will not break if the linked User is
    #deleted.
    #What will happened is that when we delete a certain user from User table,
    #All images/row that is related to this particular user will be also deleted

    #So in general whenever use pw.ForeignKeyField, because we are linking the User row/object, we should add this constraint. on_delete="Cascade"
    user=pw.ForeignKeyField(User, backref="images")
    image_url=pw.TextField(null=False)



    @hybrid_property
    def full_image_url(self):
        if self.image_url:
            from app import app
            return app.config.get("S3_LOCATION")+self.image_url
        else:
            return ""


