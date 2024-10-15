from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[Any]:
        closed_projects_query = select(CharityProject).where(
            CharityProject.fully_invested
        )
        closed_projects = await session.execute(closed_projects_query)
        projects = closed_projects.scalars().all()
        projects.sort(
            key=lambda proj: (
                proj.close_date - proj.create_date).total_seconds()
        )
        return projects


charityproject_crud = CRUDCharityProject(CharityProject)
