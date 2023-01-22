from dataclasses import dataclass
import datetime
from pathlib import Path
import yaml
from typing import Dict, List
import markdown
from markupsafe import Markup


POSTS_FOLDER = Path("posts")


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
