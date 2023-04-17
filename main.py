from typing import Any, Optional, AsyncIterator
from sqlalchemy import select, Row
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter

import schemas
import models
from database import SessionLocal


async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


app = FastAPI(title='sbserver_py',
              version='pre-alpha',
              description='Upcoming API for sb.ltn.fi. Project licensed under AGPLv3, data under CC BY-NC-SA 4.0.',
              contact={
                  'name': 'Lartza'
              },
              license_info={
                  'name': 'CC BY-NC-SA 4.0',
                  'url': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
              })


app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class SponsortimeFilter(Filter):
    videoID: Optional[str]
    order_by: Optional[list[str]]

    class Constants(Filter.Constants):
        model = models.Sponsortimes


@app.get('/vipusers', response_model=Page[schemas.Vipusers])
async def read_vipusers(db: AsyncSession = Depends(get_db)) -> Any:
    stmt = select(models.Vipusers)
    return await paginate(db, stmt)


@app.get('/vipusers/{userID}', response_model=schemas.Vipusers)
async def read_vipuser(userID: str, db: AsyncSession = Depends(get_db)) -> Optional[Row]:
    stmt = select(models.Vipusers).where(models.Vipusers.userID == userID)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.get('/sponsortimes', response_model=Page[schemas.Sponsortimes])
async def read_sponsortimes(sponsortime_filter: SponsortimeFilter = FilterDepends(SponsortimeFilter),
                            db: AsyncSession = Depends(get_db)) -> Any:
    stmt = sponsortime_filter.sort(select(models.Sponsortimes.__table__.columns, models.Usernames.userName)
                                   .outerjoin(models.Usernames,
                                              models.Sponsortimes.userID == models.Usernames.userID))
    return await paginate(db, stmt)


@app.get('/sponsortimes/{UUID}', response_model=schemas.Sponsortimes)
async def read_sponsortime(UUID: str, db: AsyncSession = Depends(get_db)) -> Optional[Row]:
    stmt = select(models.Sponsortimes).where(models.Sponsortimes.UUID == UUID)
    result = await db.execute(stmt)
    segment = result.scalar_one_or_none()
    if segment:
        return segment
    raise HTTPException(status_code=404, detail="Segment not found")


@app.get('/usernames', response_model=Page[schemas.Usernames])
async def read_usernames(db: AsyncSession = Depends(get_db)) -> Any:
    stmt = select(models.Usernames)
    return await paginate(db, stmt)


@app.get('/usernames/{userName}', response_model=Page[schemas.Usernames])
async def read_username(userName: str, db: AsyncSession = Depends(get_db)) -> Any:
    stmt = select(models.Usernames).where(models.Usernames.userName == userName)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        return user
    raise HTTPException(status_code=404, detail="Segment not found")

add_pagination(app)
