from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationList
from app.services.investment import invest_funds

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationList],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.post('/', response_model=DonationDB)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Создает новое пожертвование от текущего пользователя."""
    new_donation = await donation_crud.create(
        donation, session, user
    )
    await invest_funds(session)
    return new_donation


@router.get('/my', response_model=list[DonationDB])
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех пожертвований для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
