import os
from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '3543')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPersons(Base):
    __tablename__ = 'swapi_persons'

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column()
    eye_color: Mapped[str] = mapped_column()
    films: Mapped[str] = mapped_column()
    gender: Mapped[str] = mapped_column()
    hair_color: Mapped[str] = mapped_column()
    height: Mapped[str] = mapped_column()
    homeworld: Mapped[str] = mapped_column()
    mass: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    skin_color: Mapped[str] = mapped_column()
    species: Mapped[str] = mapped_column()
    starships: Mapped[str] = mapped_column()
    vehicles: Mapped[str] = mapped_column()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
