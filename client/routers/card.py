from aiohttp import ClientSession

from flask import (
    redirect,
    url_for,
    render_template,
    flash,
    request
)

from .. import app, API_URL

from ..schemas import (
    CreateCardForm
)

from ..utils import (
    auth_required,
    get_current_user
    )


@app.get('/add-card')
@auth_required
async def add_card_page():
    form = CreateCardForm()
    return render_template('create_card.html', form=form, account_id=request.args.get('account_id'))


@app.post('/add-card')
@auth_required
async def add_card():
    form = CreateCardForm()
    user = get_current_user()
    if form.validate_on_submit():
        async with ClientSession(API_URL) as session:
            card_data = {
                'cardholder_name': form.cardholder_name.data,
                'account_id': request.form.get('account_id'),
                'user_id': user.get('id')
            }
            async with session.post('/cards', json=card_data) as response:
                if response.status == 201:
                    flash('Вы успешно создали карту !', 'info')
                    return redirect(url_for('index'))

                flash('Не удалось создать карту', 'error')
                return render_template('create_card.html', form=form)

    return render_template('create_card.html', form=form)