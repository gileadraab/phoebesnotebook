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
class Post:

    """Class representing a single post

    Attributes:
        content (str): HTML containing the body of the post
        date (datetime.datetime): date the post is published
        draft(bool): defines if the post is a draft, draft posts are not shown
        excerpt (str): content capped to 3000 chars
        image (str): path to the post image
        markdown_path (Path): path to the markdown file to be converted to html
        show_comments (bool): define if comments are allowed for the post
        slug (str): the post slug
        tags (List[str]): a list of tags related to the post subject
        title (str): post title
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
