from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
from flask_debugtoolbar import DebugToolbarExtension

app = Flask("sayhello")

app.config.from_pyfile("settings.py")
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
bootstrap = Bootstrap4(app)
toolbar = DebugToolbarExtension(app)

from sayhello import views,errors,commands