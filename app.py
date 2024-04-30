from os import getenv
from flask import Flask

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = getenv("SECRET_KEY")

import routes

