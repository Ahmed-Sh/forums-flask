from flask import jsonify, request, abort
from app import models
from app import app, member_store, post_store


@app.route("/api/topic/all")
def api_topic_get_all():
    posts = [post.__dict__() for post in post_store.get_all()]
    return jsonify(posts)


@app.route("/api/topic/add", methods=["POST"])
def api_topic_create():
    request_data = request.get_json()
    try:
        new_post = models.Post(request_data["title"], request_data["content"])
        post_store.add(new_post)
        result = jsonify(new_post.__dict__())
    except KeyError:
        result = abort(400, "Couldn't parse the request data !")
    return result


@app.route("/api/topic/show/<int:id>", methods=["GET"])
def api_topic_show(id):
    post = post_store.get_by_id(id)
    try:
        result = jsonify(post.__dict__())
    except AttributeError:
        result = abort(404, "topic with id: %d doesn't exist" % id)
    return result


@app.route("/api/topic/delete/<int:id>", methods=["DELETE"])
def api_topic_delete(id):
    try:
        result = post_store.delete(id)
        result = jsonify(result.__dict__())
    except ValueError:
        result = abort(404, "topic with id: %d doesn't exist" % id)
    return result


@app.route("/api/topic/edit/<int:id>", methods=["PUT"])
def api_topic_edit(id):
    request_data = request.get_json()
    post = post_store.get_by_id(id)
    try:
        post.title = request_data["title"]
        post.content = request_data["content"]
        post_store.update(post)
        result = jsonify(post.__dict__())
    except AttributeError:
        result = abort(404, "topic with id: %d doesn't exist" % id)
    except KeyError:
        result = abort(400, "Couldn't parse the request data !")
    return result


@app.errorhandler(400)
def bad_request(error):
    return jsonify(message=error.description)
