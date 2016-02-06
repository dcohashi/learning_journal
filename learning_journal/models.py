from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    DateTime,
    func,
    )

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
    title = Column(Unicode(255), unique=True)
    body = Column(Unicode, nullable=True)
    created = Column(DateTime(timezone=False), default=func.now())
    edited = Column(DateTime(timezone=False), default=func.now())

def all(cls):
    '''
    Return all records sorted by created date
    '''
    query = cls.query(Entry.id, Entry.title, Entry.body, Entry.created, Entry.edited)
    query.sort(key = operator.itemgetter('created'))
    return(query)

def by_id(cls,id):
    '''
    return record for the specified id
    '''
    entry = cls.query(Entry).filter(Entry.id == id)
    return(entry)


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)
