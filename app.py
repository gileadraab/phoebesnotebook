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
