from phoebesnotebook.models import PageMultiPost, Post, Site
from phoebesnotebook.app import app
from flask import render_template


@app.route("/")
def index():
    """Renders the template for the home page, containig all posts"""
    site = Site.load_from_yaml()

    posts = Post.load_all()

    page = PageMultiPost.build(site)

    html = render_template(
        "default.html",
        site=site,
        page=page,
        posts=posts,
        body_template="index.html",
    )
    return html
