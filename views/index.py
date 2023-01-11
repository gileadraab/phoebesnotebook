@app.route("/")
def index():
    """Renders the home view, containig all posts"""
    site = load_site_config()

    post_yamls = load_post_ymls()

    posts = [Post(**post_yaml) for post_yaml in post_yamls.values()]
    print(len(posts))
    posts.sort(key=lambda post: post.date, reverse=True)

    paginator = {"posts": posts}

    page = Page(
        title=site["title"],
        title_share=site["title"],
        description=site["description"],
        image=site["avatar"],
        url="",
    )

    html = render_template(
        "default.html",
        site=site,
        page=page,
        body_template="index.html",
        paginator=paginator,
    )
    return html
