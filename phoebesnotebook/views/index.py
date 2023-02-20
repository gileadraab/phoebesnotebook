from typing import List

from flask import render_template

from phoebesnotebook.app import app
from phoebesnotebook.models import Page, PageMultiPost, Post, Site


@app.route("/")
def index():
    """Renders the template for the home page, containig all posts"""
    site: Site = Site.load_from_yaml()

    posts: List[Post] = Post.load_all()

    page: Page = PageMultiPost.build(site)

    html = render_template(
        "default.html",
        site=site,
        page=page,
        posts=posts,
        body_template="index.html",
    )
    return html
