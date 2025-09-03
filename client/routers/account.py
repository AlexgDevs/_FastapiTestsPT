from aiohttp import ClientSession

from flask import (
    redirect,
    url_for,
    render_template,
    flash
)

from .. import app, API_URL

from ..schemas import (
    CreateAccountForm
)

from ..utils import (
    auth_required,
    get_current_user
    )


@app.get('/add-account')
@auth_required
async def add_account_page():
    form = CreateAccountForm()
    return render_template('create_account.html', form=form)


@app.post('/add-account')
@auth_required
async def add_account():
    form = CreateAccountForm()
    user = get_current_user()
    if form.validate_on_submit():
        async with ClientSession(API_URL) as session:

            account_data = {
                'account_name': form.account_name.data,
                'user_id': user.get('id')
            }

            async with session.post('/accounts', json=account_data) as response:
                if response.status == 201:
                    flash('Вы успешно завели счет !', 'info')
                    return redirect(url_for('index'))

                flash('Не удалось создать счет', 'error')
                return render_template('create_account.html', form=form)

    return render_template('create_account.html', form=form)