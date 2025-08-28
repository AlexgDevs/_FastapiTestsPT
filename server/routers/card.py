from . import (
    APIRouter,
    status,
    HTTPException,
    List,
    Depends
)

from ..db import (
    select,
    Card,
    DBHelper,
    AsyncSession,
    get_session,
    joinedload,
    get_session_begin
)

from ..schemas import (
    CardResponse,
    CreateCardModel)

card_app = APIRouter(prefix='/cards', tags=['Cards'])


@card_app.get('/',
            response_model=List[CardResponse],
            summary='Get all cards',
            description='endpoint for getting all cards from accounts')
async def get_cards(session: AsyncSession = Depends(get_session)):
    cards = await session.scalars(
        select(Card)
        .options(
            joinedload(Card.user)
        )
    )
    return cards.unique().all()


@card_app.get('/{user_id}',
            response_model=List[CardResponse],
            summary='Get all cards by user',
            description='endpoint for getting all cards for user id')
async def get_cards_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    cards = await session.scalars(
        select(Card)
        .where(Card.user_id == user_id)
        .options(
            joinedload(Card.user))
    )
    return cards.unique().all()


@card_app.get('/{user_id}/{card_id}',
            response_model=CardResponse,
            summary='Get card by card and user id',
            description='endpoint for getting card by card and user id')
async def get_card_by_card_id(user_id: int, card_id: int):
    card = await DBHelper.get_card(user_id, card_id)
    if card:
        return card

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Card not found'
    )


@card_app.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Created card',
            description='endpoind for creating card for account')
async def create_card(card_data: CreateCardModel, session: AsyncSession = Depends(get_session_begin)):
    session.add(Card(**card_data.model_dump()))
    return {'status': 'created'}


@card_app.delete('/{user_id}/{card_id}',
                summary='Delete card by card and user id',
                description='enpoind for deleted card by user and card id')
async def delete_card(user_id: int, card_id: int, session: AsyncSession = Depends(get_session_begin)):
    card = await DBHelper.get_card(user_id, card_id)
    if card:
        await session.delete(card)
        return {'status': 'deleted'}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Card not found'
    )

