"""Main App File/Configuration"""

import os
from flask import Flask

app = Flask(
    __name__,
    instance_relative_config=False,
    template_folder="templates",
    static_folder="static"
)

from app.routes import *

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
