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
    id = Column('id', Integer, primary_key=True)
    Column('title',Unicode(255), unique=True)
    Column('body',Unicode, nullable=True)
    Column('created',DateTime(timezone=False), default=func.now())
    Column('edited', DateTime(timezone=False), default=func.now(), onupdate=func.now())

    def all(cls):
        '''
        Return all records sorted by created date
        '''
        all_records = cls.query.all()
        all_records.sort(key=operator.itemgetter('created'), reverse=True)
        return all_records 

    def by_id(cls,id):
        '''
        return record for the specified id
        '''
        entry = cls.query(Entry).get(id)
        return entry


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)
