from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    DateTime,
    func,
    desc,
    )
import datetime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension
import operator

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False, unique=True)
    body = Column(Unicode, nullable=True)
    created = Column(DateTime(timezone=False), 
                              default=datetime.datetime.utcnow)
    edited = Column(DateTime(timezone=False), 
                             default=datetime.datetime.utcnow, 
                             onupdate=datetime.datetime.utcnow)

    @classmethod
    def all(cls, session=None):
        '''
        Return all records sorted by created date
        '''
        if session is None:
            session = DBSession
        all_records = session.query(cls)
        all_records = all_records.order_by(desc(cls.created))
        return all_records


    @classmethod
    def by_id(cls, id, session=None):
        '''
        return record for the specified id
        '''
        if session is None:
            session = DBSession
        all_records = session.query(cls)
        entry = all_records.get(id)
        return entry


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(255), nullable=False, unique=True, index=True)
    password = Column(Unicode, nullable=False)

    @classmethod
    def user(cls, name, session=None):
        if session is None:
            session = DBSession
        all_records = session.query(cls)
        entry = all_records.get(name)
        return entry


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)
