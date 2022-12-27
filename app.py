from flask import Flask, render_template, request, url_for
import yaml

app = Flask(__name__)

@app.route("/")
def index():
  with open("config/config.yml", "r") as stream:
    site = yaml.safe_load(stream)

  page = {
    "url": "/"
  }
  content = "Hello world"

  html= render_template("default.html", site=site, page=page, content=content )
  return html


@app.route("/about")
def about():
  with open("config/config.yml", "r") as stream:
    site = yaml.safe_load(stream)

  page = {
    "url": "/about"
  }

  content = "ABOUT"

  html= render_template("default.html", site=site, page=page, content=content )
  return html

@app.route("/mypost")
def post():
  with open("config/config.yml", "r") as stream:
    site = yaml.safe_load(stream)

  page = {
    "url": "/mypost"
  }


  html= render_template("post.html", site=site, page=page)
  return html