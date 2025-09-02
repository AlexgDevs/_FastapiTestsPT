from aiohttp import ClientSession
from flask import redirect, render_template, url_for

from ..utils import auth_required, get_current_user
from .. import app, API_URL

@app.get('/')
@auth_required
async def index():
    user = get_current_user()
    async with ClientSession(API_URL) as session:
        async with session.get(f'/users/{user.get('id')}') as response:
            if response.status == 200:
                return render_template('dashboard.html', user=await response.json())

            return redirect(url_for('login_page'))
