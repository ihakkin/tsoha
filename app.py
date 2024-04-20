from flask import Flask
from os import getenv


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = getenv("SECRET_KEY")

import routes

