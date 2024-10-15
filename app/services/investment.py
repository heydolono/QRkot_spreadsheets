from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import CharityProject, Donation


async def invest_funds(session: AsyncSession):
    open_projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested.is_(False))
    )
    open_projects = open_projects.scalars().all()
    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested.is_(False))
    )
    donations = donations.scalars().all()
    for donation in donations:
        for project in open_projects:
            available_funds = donation.full_amount - donation.invested_amount
            required_funds = project.full_amount - project.invested_amount
            if available_funds > 0 and required_funds > 0:
                invest_amount = min(available_funds, required_funds)
                project.invested_amount += invest_amount
                donation.invested_amount += invest_amount
                if project.invested_amount == project.full_amount:
                    project.fully_invested = True
                    project.close_date = datetime.now()
                if donation.invested_amount == donation.full_amount:
                    donation.fully_invested = True
                    donation.close_date = datetime.now()
    await session.commit()
    for project in open_projects:
        await session.refresh(project)
    for donation in donations:
        await session.refresh(donation)
