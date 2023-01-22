from dataclasses import dataclass
from typing import Dict, List
from pathlib import Path
import yaml

SITE_CONFIG_FILEPATH = Path("config") / "config.yml"


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
