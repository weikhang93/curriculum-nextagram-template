from models.user import User
from models.base_model import BaseModel
import peewee as pw


# i forgot to inherit basemodel and tried to python migrate.py, and nth happen, database is 
# up to date. 
#After i inherit Basemodel and migrate, it works, the reason is Basemodal is where we actually connect
#our python file , which in this case ALL our models to postgresql.
class FanIdol(BaseModel):
    idol=pw.ForeignKeyField(User, backref="fan")
    fan=pw.ForeignKeyField(User, backref="idol")
    is_approved=pw.BooleanField(default=False)


  

#Before i do the conditional rendering for the "FRONTEND" to not show the followmebabeh button,
#The fan can keep on spamming follow and it will create multiple line of the same data in our db which
#We don't want....

# So there are 3 ways we can solve this
# 1)frontend ( conditional rendering, dont let them press the button after they followed it.)
# 2)backend (check if the exact same row of data exist in the db, if it exist, then dont .save() it.)
# 3)Do some modification on the model/table itself. http://docs.peewee-orm.com/en/latest/peewee/models.html#indexes-and-constraints
#   search for multi-column-indexes. Need to have another class Meta() inside our FanIdol

# For an better app experience, just do the conditional rendering on the frontend
# For a more secured app, add the class Meta() inside our FanIdol class. Cause even if we did the 
# checking for solution (2), hacker can still skip the view function and straight away .create an 
# copy of existing instance in our DB(assuming they can connect to our db).
