from __future__ import annotations

import datetime
import functools
from dataclasses import dataclass
from pathlib import Path
from typing import List

import markdown
import yaml
from markupsafe import Markup

POSTS_FOLDER = Path("posts")


@dataclass
class Post:

    """Class representing a single post

    Attributes:
        content (str): HTML containing the body of the post
        date (datetime.datetime): Date the post is published
        draft(bool): If this is True posts are not shown anywhere
        excerpt (str): A short preview of the post
        (used in the index page instead of the full post)
        excerpt_length (int): Define the number of chars contained in an excerpt
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
    excerpt_length: int

    @classmethod
    def load_all(cls) -> List[Post]:
        """Read all the yaml files corresponding to posts
        and store them in a dict whose key is the slug of each post
        and the value is the content of the yaml file an then convert
        them into list of posts"""
        post_yamls = {}
        for file in POSTS_FOLDER.glob("*.yml"):
            with open(file, "r") as stream:
                post_yaml = yaml.safe_load(stream)
                post_yamls[post_yaml["slug"]] = post_yaml
                posts = [Post(**post_yaml) for post_yaml in post_yamls.values()]
                posts.sort(key=lambda post: post.date, reverse=True)
                posts = list(filter(lambda post: post.draft is False, posts))
        return posts

    @property
    def excerpt(self):
        return self.content[0 : self.excerpt_length]

    @functools.cached_property
    def content(self):
        extensions = [
            "fenced_code",
            "toc",
            "codehilite",
            "pymdownx.arithmatex",
        ]

        with open(self.markdown_path, "r", encoding="utf-8") as post:
            return Markup(
                markdown.markdown(
                    post.read(),
                    extensions=extensions,
                )
            )

    def __post_init__(self):
        self.date = datetime.datetime.strptime(self.date, "%d/%m/%y %H:%M")
        self.markdown_path = POSTS_FOLDER / self.markdown_path
