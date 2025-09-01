from flask import Flask
from server import API_URL

app = Flask(__name__, template_folder='templates')
app.secret_key = '123_user_123'


from . import routers