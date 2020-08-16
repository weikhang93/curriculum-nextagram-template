from flask import Blueprint , jsonify
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    #basically jsonify is a function that take in something(in this case its dictionary) and render it out as an json format instead of html.
    

    users=User.select().order_by(User.id)
    result=[]
    for user in users:
        result.append(
            {
                "id":user.id,
                "profileImage":user.full_image_path,
                "username":user.username
            
        }
        )
    return jsonify(result)

@users_api_blueprint.route('/<id>')
# the reason why we use show is because its for a specific user.
def show(id):
    
    user=User.get_or_none(User.id==int(id))
    result={"id":user.id,
            "profileImage":user.full_image_path,
            "username":user.username}
    return jsonify(result)