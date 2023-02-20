from typing import List

from flask import render_template

from phoebesnotebook.app import app
from phoebesnotebook.models import Page, PageSinglePost, Post, Site


@app.route("/post/<slug>")
def post(slug: str):
    """Renders the template for a specific post (defined by the slug)"""
    site: Site = Site.load_from_yaml()

    posts: List[Post] = Post.load_all()
    post: Post = list(filter(lambda post: post.slug == slug, posts))[0]

    page: Page = PageSinglePost.build(site, post, slug)
    print(page.image)

    html = render_template(
        "default.html", site=site, page=page, post=post, body_template="post.html"
    )
    return html
