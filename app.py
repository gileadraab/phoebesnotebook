from phoebesnotebook.joao.romario import my_func
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

    @classmethod
    def load_from_yaml(cls) -> dict:
        """Read main .yaml file containig high level website settings"""
        with open(SITE_CONFIG_FILEPATH, "r") as file:
            site = yaml.safe_load(file)
        return Site(**site)


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

    @classmethod
    def load_all(cls) -> dict:
        """Read all the yaml files corresponding to posts, and store them in a dict whose key is the slug of each post and the value is the content of the yaml file"""
        post_yamls = {}
        for file in POSTS_FOLDER.glob("*.yml"):
            with open(file, "r") as stream:
                post_yaml = yaml.safe_load(stream)
                post_yamls[post_yaml["slug"]] = post_yaml
                posts = [Post(**post_yaml) for post_yaml in post_yamls.values()]
                posts.sort(key=lambda post: post.date, reverse=True)
                posts = list(filter(lambda post: post.draft == False, posts))
        return posts

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
class Page:
    title: str
    title_share: str
    description: str
    url: str
    image: str


class PageSinglePost(Page):
    @classmethod
    def build(cls, site: Site, post: Post, slug: str):
        return PageSinglePost(
            title=f"{post.title} | {site.title}",
            title_share=f"{post.title} | {site.title}",
            description=post.excerpt,
            image=url_for("static", filename=f"images/posts/{slug}/{post.image}"),
            url=f"post/{slug}",
        )


class PageMultiPost(Page):
    @classmethod
    def build(cls, site: Site):
        return PageMultiPost(
            title=site.title,
            title_share=site.title,
            description=site.description,
            image=site.avatar,
            url="",
        )


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
