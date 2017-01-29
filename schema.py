__author__ = 'gautham'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Text, ForeignKey, Float, DateTime, func, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import ForeignKeyConstraint
import datetime

Base = declarative_base()


class Band(Base):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    language = Column(String(100))
    info = Column(Text)


class Year(Base):
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True)
    name = Column(Integer)


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(Text)


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    language = Column(String(100))
    info = Column(Text)
    band_id = Column(Integer)#, ForeignKey('bands.id'))
    band_name = Column(String(100))#, ForeignKey('bands.name'))

    band = relationship('Band', backref=backref('albums'))

    __table_args__ = (
                      ForeignKeyConstraint(['band_id'],['bands.id']),
                     )


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    file = Column(Text)
    title = Column(Text)
    album_id = Column(Integer, ForeignKey('albums.id'))
    band_id = Column(Integer, ForeignKey('bands.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    artist = Column(Text)
    # track number
    track = Column(Integer)
    plays = Column(Integer, default=0)
    year_id = Column(Integer)
    length = Column(Integer)
    lyrics = Column(Text)
    creation_time = Column(Integer, default=0)
    status_add = Column(Boolean)

    album = relationship('Album', backref=backref('tracks'))
    genre = relationship('Genre', backref=backref('tracks'))
    bands = relationship('Band', backref=backref('tracks'))
