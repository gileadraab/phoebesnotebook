import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import markdown
import yaml
from flask import Flask, render_template, request, url_for
from jinja2 import Environment, FileSystemLoader, StrictUndefined, Template
from markupsafe import Markup

app = Flask(__name__)
SITE_CONFIG_FILEPATH = Path("config") / "config.yml"
POSTS_FOLDER = Path("posts")
TEMPLATES_FOLDER = Path("templates")


def render_template_strict(template_filename: str, **kwargs):
    """Summary

    Args:
        template_filename (str): Description
        **kwargs: Description

    Returns:
        TYPE: Description
    """
    with open(TEMPLATES_FOLDER / template_filename, "r", encoding="utf-8") as html_file:
        html = html_file.read()

    template = Environment(
        loader=FileSystemLoader(TEMPLATES_FOLDER), undefined=StrictUndefined
    ).from_string(html)

    return template.render(**kwargs)


def load_site_config() -> dict:
    """Read main .yaml file containig high level website settings"""
    with open(SITE_CONFIG_FILEPATH, "r") as file:
        site = yaml.safe_load(file)
    return site


def load_post_ymls() -> dict:
    """Read all the yaml files corresponding to posts, and store them in a dict whose key is the slug of each post and the value is the content of the yaml file"""
    post_yamls = {}
    for file in POSTS_FOLDER.glob("*.yml"):
        with open(file, "r") as stream:
            post_yaml = yaml.safe_load(stream)
        if not post_yaml["draft"]:
            post_yamls[post_yaml["slug"]] = post_yaml

    return post_yamls


def load_post_ymls_by_tag(tag: str) -> dict:
    """Read all the yaml files corresponding to posts, and store the ones that matches an specific tag in a dict whose key is the slug of each post and the value is the content of the yaml file"""
    tagged_post_yamls = {}
    for file in POSTS_FOLDER.glob("*.yml"):
        with open(file, "r") as stream:
            post_yaml = yaml.safe_load(stream)
        if tag in post_yaml["tags"]:
            tagged_post_yamls[post_yaml["slug"]] = post_yaml

    return tagged_post_yamls


@dataclass
class Post:

    """Class representing a single post

    Attributes:
        content (str): HTML containing the body of the post
        date (datetime.datetime): Date the post is published
        draft(bool): If this is True posts are not shown anywhere
        excerpt (str): A short preview of the post (used in the index page instead of the full post)
        image (str): Image filename
        markdown_path (Path): Path to the markdown file to be converted to html
        show_comments (bool): Define if comments are allowed for the post
        slug (str): The post slug
        tags (List[str]): A list of tags related to the post subject
        title (str): Post title

    """

    title: str
    date: datetime.datetime
    image: str
    markdown_path: Path
    tags: List[str]
    show_comments: bool
    slug: str
    draft: bool

    def __init__(
        self, title, date, image, markdown_path, tags, show_comments, slug, draft
    ):
        self.title = title
        self.date = datetime.datetime.strptime(date, "%d/%m/%y %H:%M")
        self.image = image
        self.markdown_path = POSTS_FOLDER / markdown_path
        self.tags = tags
        self.show_comments = show_comments
        self.slug = slug
        self.draft = draft

    @property
    def excerpt(self):
        return self.content[0:3000]

    @property
    def excerpt(self):
        return self.content[0:3000]

    @property
    def content(self):
        # can we cache this?
        with open(self.markdown_path, "r", encoding="utf-8") as post:
            return Markup(
                markdown.markdown(
                    post.read(),
                    extensions=[
                        "fenced_code",
                        "toc",
                        "codehilite",
                        "pymdownx.arithmatex",
                    ],
                )
            )


@dataclass
class Site:
    title: str
    name: str
    job_title: str
    email: str
    description: str
    avatar: str
    favicon: str
    twitter_handler: str
    analytics_code: str
    disqus: str
    pages: List[Dict]
    social_networks: List[Dict]
    show_tags: bool
    show_email: bool
    show_rss: bool
    show_comments: bool
    show_menu: bool
    fixed_sidebar: bool


@dataclass
class Page:
    title: str
    title_share: str
    description: str
    url: str
    image: str


@app.route("/")
def index():
    """Renders the template for the home page, containig all posts"""
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


@app.route("/post/<slug>")
def post(slug: str):
    """Renders the template for a specific post (defined by the slug)"""
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


@app.route("/tag/<slug>")
def tags(slug: str):
    """Renders the template for the tag page, containig all posts that matches one specific tag (defined by the slug)"""
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


# @app.route("/about")
# def about():
#   with open("config/config.yml", "r") as stream:
#     site = yaml.safe_load(stream)

#   page = {
#     "url": "/about"
#   }

#   content = "ABOUT"

#   html= render_template("default.html", site=site, page=page, content=content )
#   return html
