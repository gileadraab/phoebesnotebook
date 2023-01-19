@app.route("/tag/<slug>")
def tags(slug: str):
    """Renders the template for the tag page, containig all posts that matches one specific tag (defined by the slug)"""
    site = Site.load_from_yaml()

    posts = Post.load_all()
    posts = list(filter(lambda post: slug in post.tags, posts))

    page = PageMultiPost.build(site)

    html = render_template(
        "default.html", site=site, page=page, posts=posts, body_template="index.html"
    )
    return html
