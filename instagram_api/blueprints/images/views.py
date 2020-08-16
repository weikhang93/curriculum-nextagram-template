from flask import Blueprint
from models.images import Images


images_api_blueprint=Blueprint("images_api",
                                __name__,
                                template_folder="templates")


@images_api_blueprint.route("/me")
def index():
    pass


