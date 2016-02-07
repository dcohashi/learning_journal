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
    created = Column(DateTime(timezone=False), default=func.now())
    edited = Column(DateTime(timezone=False), default=func.now(), onupdate=func.now())

    @classmethod
    def all(cls):
        '''
        Return all records sorted by created date
        '''
        all_records = DBSession.query(cls)
        all_records = all_records.order_by(desc(cls.created))
        return all_records


    @classmethod
    def by_id(cls, id):
        '''
        return record for the specified id
        '''
        all_records = DBSession.query(cls)
        entry = all_records.get(id)
        return entry


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)
