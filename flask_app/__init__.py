from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app = Flask(__name__)

app.secret_key="goober"