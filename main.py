from os import environ
from databases import Database
from sqlalchemy import create_engine

from fastapi import FastAPI, Query
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.databases import paginate
from fastapi.middleware.cors import CORSMiddleware

import models
import tables

env = environ.get('APPLICATION_ENV')
if env == 'production':
    DATABASE_URL = f"postgresql://sponsorblock:{environ['DB_PASSWORD']}@/sponsorblock?host=/run/postgresql"
elif env == 'test':
    DATABASE_URL = "sqlite:///./test.db"
else:  # development
    DATABASE_URL = 'postgresql://sponsorblock@127.0.0.1/sponsorblock'

database = Database(DATABASE_URL)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
tables.metadata.create_all(engine)


def filter_sponsortimes(**kwargs):
    query = kwargs['query']
    if kwargs['UUID'] is not None:
        query = query.where(tables.sponsortimes.c.UUID == kwargs['UUID'])
    if kwargs['videoID'] is not None:
        query = query.where(tables.sponsortimes.c.videoID == kwargs['videoID'])
    if kwargs['userID'] is not None:
        query = query.where(tables.sponsortimes.c.userID == kwargs['userID'])
    if kwargs['shadowHidden'] is not None:
        if kwargs['shadowHidden']:
            query = query.where(tables.sponsortimes.c.shadowHidden == 1)
        else:
            query = query.where(tables.sponsortimes.c.shadowHidden == 0)
    if kwargs['votes_from'] is not None:
        query = query.where(tables.sponsortimes.c.votes >= kwargs['votes_from'])
    if kwargs['votes_to'] is not None:
        query = query.where(tables.sponsortimes.c.votes <= kwargs['votes_to'])
    if kwargs['views_from'] is not None:
        query = query.where(tables.sponsortimes.c.views >= kwargs['views_from'])
    if kwargs['views_to'] is not None:
        query = query.where(tables.sponsortimes.c.views <= kwargs['views_to'])
    if kwargs['category'] is not None:
        query = query.where(tables.sponsortimes.c.category.in_(kwargs['category']))
    return query


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


@app.on_event('startup')
async def startup() -> None:
    await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    await database.disconnect()


@app.get('/vipusers', response_model=Page[models.Vipusers])
async def read_vipusers():
    query = tables.vipusers.select()
    return await paginate(database, query)


@app.get('/vipusers/{userID}', response_model=models.Vipusers)
async def read_vipuser(userID: str):
    query = tables.vipusers.select().where(tables.vipusers.c.userID == userID)
    return await database.fetch_one(query)


@app.get('/sponsortimes', response_model=models.SponsortimeListPaginated)
async def read_sponsortimes(videoID: str | None = None, votes_from: int | None = None, votes_to: int | None = None,
                            views_from: int | None = None, views_to: int | None = None,
                            category: list[str] | None = Query(None), shadowHidden: bool | None = None,
                            UUID: str | None = None, userID: str | None = None,
                            size: int = Query(10, ge=1, le=100), next_page_token: int | None = None):
    query = tables.sponsortimes.select()
    query = filter_sponsortimes(**locals())
    if next_page_token is None:
        query = query.order_by(tables.sponsortimes.c.timeSubmitted.desc()).limit(size)
    else:
        query = (
            query
            .where(tables.sponsortimes.c.timeSubmitted < next_page_token)
            .order_by(tables.sponsortimes.c.timeSubmitted.desc())
            .limit(size)
        )
    result = await database.fetch_all(query)
    if len(result) < size:
        next_page_token = None
    else:
        next_page_token = result[size - 1]["timeSubmitted"]
    return {"items": result, "next_page_token": next_page_token, "size": size}


@app.get('/sponsortimes/{UUID}', response_model=models.Sponsortimes)
async def read_sponsortime(UUID: str):
    query = tables.sponsortimes.select().where(tables.sponsortimes.c.UUID == UUID)
    return await database.fetch_one(query)


@app.get('/usernames', response_model=Page[models.Usernames])
async def read_usernames(sort: list[str] = Query(['-userName'])):
    query = tables.usernames.select()
    for s in sort:
        if s.startswith('-'):
            query = query.order_by(getattr(tables.usernames.c, s[1:]).desc())
        else:
            query = query.order_by(getattr(tables.usernames.c, s).asc())
    return await paginate(database, query)


@app.get('/usernames/{userName}', response_model=Page[models.Usernames])
async def read_usernames(userName: str, sort: list[str] = Query(['-userName'])):
    query = tables.usernames.select().where(tables.usernames.c.userName == userName)
    for s in sort:
        if s.startswith('-'):
            query = query.order_by(getattr(tables.usernames.c, s[1:]).desc())
        else:
            query = query.order_by(getattr(tables.usernames.c, s).asc())
    return await paginate(database, query)


@app.get('/usernames/{userName}/sponsortimes', response_model=Page[models.Sponsortimes])
async def read_sponsortimes(userName: str, videoID: str | None = None, votes_from: int | None = None,
                            votes_to: int | None = None, views_from: int | None = None, views_to: int | None = None,
                            category: list[str] | None = Query(None), shadowHidden: bool | None = None,
                            UUID: str | None = None, userID: str | None = None,
                            sort: list[str] = Query(['-timeSubmitted'])):
    usernames_list = []
    rows = await database.fetch_all(tables.usernames.select().where(tables.usernames.c.userName == userName))
    for row in rows:
        usernames_list.append(row['userID'])
    query = tables.sponsortimes.select().where(tables.sponsortimes.c.userID.in_(usernames_list))
    query = filter_sponsortimes(**locals())
    for s in sort:
        if s.startswith('-'):
            query = query.order_by(getattr(tables.sponsortimes.c, s[1:]).desc())
        else:
            query = query.order_by(getattr(tables.sponsortimes.c, s).asc())
    return await paginate(database, query)


@app.get('/config', response_model=list[models.Config])
async def read_config():
    query = tables.config.select()
    return await database.fetch_all(query)


@app.get('/users/{userID}/username', response_model=models.Usernames)
async def read_username(userID: str):
    query = tables.usernames.select().where(tables.usernames.c.userID == userID)
    return await database.fetch_one(query)


@app.get('/users/{userID}/sponsortimes', response_model=Page[models.Sponsortimes])
async def read_sponsortimes(userID: str, videoID: str | None = None, votes_from: int | None = None,
                            votes_to: int | None = None, views_from: int | None = None, views_to: int | None = None,
                            category: list[str] | None = Query(None), shadowHidden: bool | None = None,
                            UUID: str | None = None, sort: list[str] = Query(['-timeSubmitted'])):
    query = tables.sponsortimes.select()
    query = filter_sponsortimes(**locals())
    for s in sort:
        if s.startswith('-'):
            query = query.order_by(getattr(tables.sponsortimes.c, s[1:]).desc())
        else:
            query = query.order_by(getattr(tables.sponsortimes.c, s).asc())
    return await paginate(database, query)


add_pagination(app)
