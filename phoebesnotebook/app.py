# from pathlib import Path
from flask import Flask

# from jinja2 import Environment, FileSystemLoader, StrictUndefined, Template


app = Flask(__name__)
from phoebesnotebook.views import index, post, tagged


# TEMPLATES_FOLDER = Path("templates")


# def render_template_strict(template_filename: str, **kwargs):
#     """Summary

#     Args:
#         template_filename (str): Description
#         **kwargs: Description

#     Returns:
#         TYPE: Description
#     """
#     with open(TEMPLATES_FOLDER / template_filename, "r", encoding="utf-8") as html_file:
#         html = html_file.read()

#     template = Environment(
#         loader=FileSystemLoader(TEMPLATES_FOLDER), undefined=StrictUndefined
#     ).from_string(html)

#     return template.render(**kwargs)
