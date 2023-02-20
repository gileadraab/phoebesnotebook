from flask import Flask

app = Flask(__name__)
from phoebesnotebook.views import index, post, tagged  # noqa: E402,F401
