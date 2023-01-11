@app.route("/post/<slug>")
def post(slug: str):
    """Renders a view for an specific post (defined by the slug)"""
    site = load_site_config()

    post_yamls = load_post_ymls()

    posts = [Post(**post_yaml) for post_yaml in post_yamls.values()]

    post_yaml = post_yamls[slug]

    post = Post(**post_yaml)

    paginator = {"posts": posts}

    page = Page(
        title=f'{post.title} | {site["title"]}',
        title_share=f'{post.title} | {site["title"]}',
        description=post.excerpt,
        image=url_for("static", filename=f"images/posts/{slug}/{post.image}"),
        url=f"post/{slug}",
    )

    html = render_template(
        "default.html",
        site=site,
        page=page,
        post=post,
        body_template="post.html",
        paginator=paginator,
    )
    return html
