from flask import Blueprint , request


login_api_blueprint=Blueprint('login_api',
                              __name__,
                              template_folder="templates")


@login_api_blueprint.route("/login" , methods=["POST"])
def login():
    #At our react app, whenever we use axios / ajax, they automatically send those data as json
    username=request.json.get('username')
    password=request.json.get('password')
    

    
    return "hehehe"
