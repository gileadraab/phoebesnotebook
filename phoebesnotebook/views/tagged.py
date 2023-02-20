from typing import List

from flask import render_template

from phoebesnotebook.app import app
from phoebesnotebook.models import Page, PageMultiPost, Post, Site


@app.route("/tag/<slug>")
def tagged(slug: str):
    """Renders the template for the tag page,
    containig all posts that matches one specific tag (defined by the slug)"""
    site: Site = Site.load_from_yaml()

    posts: List[Post] = Post.load_all()
    posts = list(filter(lambda post: slug in post.tags, posts))

    page: Page = PageMultiPost.build(site)

    html = render_template(
        "default.html", site=site, page=page, posts=posts, body_template="index.html"
    )
    return html
