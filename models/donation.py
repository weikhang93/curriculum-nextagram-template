import peewee as pw
from models.base_model import BaseModel
from models.images import Images
from models.user import User






class Donation(BaseModel):
    amount=pw.IntegerField()
    image=pw.ForeignKeyField(Images, backref="abc")  ##in the future should change the backref to donations , same goes for backref for sender
    sender=pw.ForeignKeyField(User, backref="abc")