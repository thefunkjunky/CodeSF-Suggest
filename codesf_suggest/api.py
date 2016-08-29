import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from .main import app
from .database import session


### Define the API endpoints
############################
# GET endpoints
############################


def check_post_id(post_id):
    post = session.query(models.Post).get(post_id)
    if not post:
        message = "Could not find post with id {}".format(post_id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

def check_user_id(user_id):
    user = session.query(models.User).get(user_id)
    if not user:
        message = "Could not find user with id {}".format(user_id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

@app.route("api/posts", methods=["GET"])
@app.route("api/users/<int:user_id>/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get(user_id=None):
    """ Returns a list of posts """

    if user_id:
        check_user_id(user_id)

    posts = session.query(models.Post)
    posts = posts.order_by(models.Post.id)

    if not posts:
        message = "No posts in database."
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps([post.as_dictionary() for post in posts],
        default=json_serial)
    return Response(data, 200, mimetype="application/json")

@app.route("api/posts/<int:post_id>" methods=["GET"])
@decorators.accept("application/json")
def post_get(post_id):
    """ Returns a specific post """

    check_post_id(post_id)

    post = session.query(models.Post).get(post_id)

    # Check for post's existence
    if not post:
        message = "Could not find post with id {}".format(post_id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps(post.as_dictionary(), default=json_serial)
    return Response(data, 200, mimetype="application/json")

@app.route("/api/users/<int:user_id>", methods=["GET"])
@decorators.accept("application/json")
def user_get(user_id):
    """ Returns User data """

    check_user_id(user_id)

    user = session.query(models.User).get(user_id)

    if not user:
        message = "Could not find user with id #{}".format(user_id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps(user.as_dictionary(), default=json_serial)
    return Response(data, 200, mimetype="application/json")



