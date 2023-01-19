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
