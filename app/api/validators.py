from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models import CharityProject


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charityproject_crud.get(obj_id=project_id, session=session)
    return project


async def check_project_unique(
        project_name: int,
        session: AsyncSession,
) -> CharityProject:
    project_id = await charityproject_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_delete_project(
        project_id: int,
        session: AsyncSession,
) -> None:
    project = await charityproject_crud.get(obj_id=project_id, session=session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Проект не найден"
        )
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!"
        )
    if project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект закрыт!"
        )


async def check_update_project(
        project_id: int,
        new_amount: int,
        session: AsyncSession,
) -> None:
    project = await charityproject_crud.get(obj_id=project_id, session=session)
    if project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!"
        )
    if new_amount is not None and new_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Новая сумма не может быть меньше вложенной суммы!"
        )
