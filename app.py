from flask import Flask, render_template, request
from markupsafe import  Markup
import markdown
import datetime
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import List


app = Flask(__name__)
SITE_CONFIG_FILEPATH = Path("config") / "config.yml"
POSTS_FOLDER = Path("posts")

def load_site_config() -> dict:
  with open(SITE_CONFIG_FILEPATH, "r") as file:
    site = yaml.safe_load(file)
  return site

def load_post_ymls() -> dict:
  post_yamls = {}
  for file in POSTS_FOLDER.glob("*.yml"):
    with open(file, "r") as stream:
      post_yaml = yaml.safe_load(stream)
    post_yamls[post_yaml['slug']] = post_yaml
  
  return post_yamls

@dataclass
class Post: 
  title: str
  date: datetime.datetime
  image: str
  markdown_path: Path
  tags: List[str]
  show_comments: bool
  slug: str

  def __init__(self, title, date, image, markdown_path, tags, show_comments, slug):
    self.title = title 
    self.date = datetime.datetime.strptime(date, "%d/%m/%y %H:%M") 
    self.image = image 
    self.markdown_path = POSTS_FOLDER / markdown_path
    self.tags = tags 
    self.show_comments = show_comments
    self.slug = slug

    with open(self.markdown_path, "r", encoding="utf-8") as post:
      self.content = Markup(markdown.markdown(post.read(), extensions=['fenced_code', 'toc', 'codehilite']))
    
    self.excerpt = self.content[0:300]

@app.route("/")
def index():
  site = load_site_config()

  post_yamls = load_post_ymls()

  posts = [Post(**post_yaml) for post_yaml in post_yamls.values()]

  paginator = {
    'posts': posts
  }

  page = {
    "url": "/"
  }

  content = "Hello world"

  html= render_template("default.html", site=site, page=page, content=content, body_template="index.html", paginator=paginator )
  return html


@app.route("/post/<slug>")
def post(slug):
  site = load_site_config()

  post_yamls = load_post_ymls()

  post_yaml = post_yamls[slug]

  post = Post(**post_yaml)

  page = {
    "url": "/mypost"
  }

  html= render_template("default.html", site=site, page=page, post=post, body_template = 'post.html')
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

