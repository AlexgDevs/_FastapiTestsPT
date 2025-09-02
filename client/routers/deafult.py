from aiohttp import request
from flask import render_template

from ..utils import auth_required
from .. import app 

@app.get('/')
@auth_required
async def index():
    return render_template('__base.html')
