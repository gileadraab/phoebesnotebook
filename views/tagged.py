@app.route("/tag/<slug>")
def tags(slug: str):
    """Renders a view containing all the posts that matches one specific tag (defined by the slug)"""
    site = load_site_config()

    tagged_posts_yamls = load_post_ymls_by_tag(slug)

    posts = [Post(**post_yaml) for post_yaml in tagged_posts_yamls.values()]
    posts.sort(key=lambda post: post.date, reverse=True)

    paginator = {"posts": posts}

    page = {"url": "/"}

    html = render_template(
        "default.html",
        site=site,
        page=page,
        body_template="index.html",
        paginator=paginator,
    )
    return html
