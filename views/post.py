@app.route("/post/<slug>")
def post(slug: str):
    """Renders the template for a specific post (defined by the slug)"""
    site = Site.load_from_yaml()

    posts = Post.load_all()
    post = list(filter(lambda post: post.slug == slug, posts))
    post = post[0]

    page = PageSinglePost.build(site, post, slug)

    html = render_template(
        "default.html", site=site, page=page, post=post, body_template="post.html"
    )
    return html
