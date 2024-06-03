from contextlib import asynccontextmanager
from contextvars import Token
from enum import Enum
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Delete, Insert, Update

from core.contexts import database_session_context
from core.settings.config import settings


def get_session_context() -> str:
    return database_session_context.get()


def set_session_context(session_id: str) -> Token:
    return database_session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    database_session_context.reset(context)


class EngineType(Enum):
    READER_WRITER = "reader_writer"


engines = {
    EngineType.READER_WRITER: create_async_engine(
        settings.database_url, pool_recycle=3600
    ),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines[EngineType.READER_WRITER].sync_engine
        else:
            return engines[EngineType.READER_WRITER].sync_engine


_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)
session = async_scoped_session(
    session_factory=_async_session_factory,
    scopefunc=get_session_context,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    _session = async_sessionmaker(
        class_=AsyncSession,
        sync_session_class=RoutingSession,
        expire_on_commit=False,
    )()
    try:
        yield _session
    finally:
        await _session.close()


@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    _session = async_sessionmaker(
        class_=AsyncSession,
        sync_session_class=RoutingSession,
        expire_on_commit=False,
    )()
    try:
        yield _session
    finally:
        await _session.close()
