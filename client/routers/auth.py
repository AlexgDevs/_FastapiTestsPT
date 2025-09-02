from aiohttp import ClientSession

from flask import (
    make_response,
    redirect,
    url_for,
    render_template,
    flash
)

from .. import app, API_URL

from ..schemas import (
    RegistrationForm,
    LoginForm
)

from ..utils import (
    guest_required, 
    auth_required)


@app.get('/register-page')
@guest_required
async def register_page():
    form = RegistrationForm()
    return render_template('register.html', form=form)


@app.get('/login-page')
@guest_required
async def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.get('/logout-page')
@guest_required
async def logout_page():
    return render_template('logout.html')


@app.post('/register')
@guest_required
async def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        async with ClientSession(API_URL) as session:
            json_data = {
                'name': form.name.data,
                'email': form.email.data,
                'password': form.password.data,
            }

            async with session.post('/auth/register', json=json_data) as response:
                if response.status == 201:
                    flash('Вы успешно зарегистрировались', 'info')
                    data = await response.json()

                    flask_response = make_response(redirect(url_for('index')))
                    
                    flask_response.set_cookie(
                        'access_token', 
                        data['tokens']['access'],
                        httponly=True,
                        secure=False,
                        samesite='Lax',
                        max_age=604800
                    )
                    flask_response.set_cookie(
                        'refresh_token',
                        data['tokens']['refresh'], 
                        httponly=True,
                        secure=False,
                        samesite='Lax',
                        max_age=2592000
                    )

                    return flask_response
                
                flash('Упс, что то пошло не так. Попробуйте позднее', 'error')
                return render_template('register.html', form=form)

    return render_template('register.html', form=form)


@app.post('/login')
@guest_required
async def login():
    form = LoginForm()
    if form.validate_on_submit():
        async with ClientSession(API_URL) as session:

            json_data = {
                    'name': form.name.data,
                    'password': form.password.data
                }

            async with session.post('/auth/token', json=json_data) as response:
                if response.status == 200:
                    data = await response.json()

                    flask_response = make_response(redirect(url_for('index')))
                    flask_response.set_cookie(
                        'access_token', 
                        data['tokens']['access'],
                        httponly=True,
                        secure=False,
                        samesite='Lax',
                        max_age=604800
                    )
                    flask_response.set_cookie(
                        'refresh_token',
                        data['tokens']['refresh'], 
                        httponly=True,
                        secure=False,
                        samesite='Lax',
                        max_age=2592000
                    )

                    return flask_response 

                flash('Упс, что то пошло не так. Попробуйте позднее', 'error')
                return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.get('/logout-accept')
@auth_required
async def logout():
    flask_response = make_response(redirect(url_for('login_page')))
    flask_response.delete_cookie('access_token')
    flask_response.delete_cookie('refresh_token')
    return flask_response


@app.get('/logout-cancel')
@auth_required
async def un_logout():
    return redirect(url_for('index'))