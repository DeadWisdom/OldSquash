from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine as _create_engine
from sqlalchemy.orm import mapper, relation, sessionmaker

metadata = MetaData()

def create_engine(url, echo=False):
    engine = _create_engine(url, echo=echo)
    metadata.create_all(engine)
    engine.create_session = sessionmaker(bind=engine)
    return engine

projects_table = Table('projects', metadata,
    Column('id', Integer, primary_key=True),
    Column('slug', String),
    Column('name', String),
    Column('description', String),
)

tickets_table = Table('tickets', metadata,
    Column('id', Integer, primary_key=True),
    Column('slug', String),
    Column('name', String),
    Column('status', String),
    Column('description', String),
    Column('reporter', String),
    Column('owner', String),
    Column('type', String),
    #Column('parent_id', Integer, ForeignKey('tickets.id')),
    Column('project_id', Integer, ForeignKey('projects.id')),
)