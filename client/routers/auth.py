from .. import app, API_URL
from ..schemas import (
    RegistrationForm,
    LoginForm
)

from aiohttp import ClientSession

from flask import (
    redirect,
    url_for,
    render_template,
    flash
)

@app.get('/register-page')
async def register_page():
    form = RegistrationForm()
    return render_template('register.html', form=form)


@app.get('/login-page')
async def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.get('/logout-page')
async def logout_page():
    return render_template('logout.html')


@app.post('/register')
async def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        async with ClientSession(API_URL) as session:
            async with session.post('/auth/register') as response:
                pass 

    return render_template('register.html', form=form)


@app.post('/login')
async def login():
    form = LoginForm()
    if form.validate_on_submit():
        async with ClientSession(API_URL) as session:
            async with session.post('/auth/token') as response:
                pass 

    return render_template('login.html', form=form)


@app.get('/logout-accept')
async def logout():
    pass


@app.get('/logout-cancel')
async def un_logout():
    pass