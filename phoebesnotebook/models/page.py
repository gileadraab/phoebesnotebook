from dataclasses import dataclass

from flask import url_for

from phoebesnotebook.models.post import Post
from phoebesnotebook.models.site import Site


@dataclass
class Page:
    title: str
    title_share: str
    description: str
    image: str
    url: str


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
