from flask import Flask, render_template, request, redirect, url_for
from dbio import JSONManager
from models import Post
from typing import Optional
import logging
from flask import json
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


app = Flask(__name__)
app.debug = True
post_manager = JSONManager()


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.route("/")
@app.route("/list")
def list():
    posts = post_manager.get_posts()
    logger.info(f"posts retrieved are: {posts}")
    return render_template("list.html", posts=posts)


@app.route("/detail/<int:uid>")
def detail(uid):
    post = post_manager.inspect_post(uid)
    if post:
        return render_template("detail.html", post=post)
    return redirect(url_for("list"))


@app.route("/form")
@app.route("/form/<int:uid>")
def form(uid: Optional[int] = None):
    post = None
    if uid:
        post = post_manager.inspect_post(uid)

    return render_template("form.html", indexid=uid, post=post)


@app.route("/save", methods=["POST"])
def save():
    post = Post.fromDict(request.form)
    post_manager.insert_post(post)

    return redirect(url_for("list"))


@app.route("/update/<int:uid>", methods=["GET", "POST"])
def update(uid):
    post = Post.fromDict(request.form)
    post_manager.update_post(uid, post)
    return redirect(url_for("list"))


@app.route("/delete/<int:uid>", methods=["GET"])
def delete(uid):
    post_manager.delete_post(uid)
    return redirect(url_for("list"))
