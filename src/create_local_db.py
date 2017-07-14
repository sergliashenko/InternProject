from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.dialects.postgresql import JSON
import json

engine = create_engine("postgres://postgres:postgres@localhost:5432/upwork_data")
if not database_exists(engine.url):
    create_database(engine.url)
    if database_exists(engine.url):
        print("DB is created")
else:
    print("DB Already exist")


Base = declarative_base()

# table_name = "upwork_info"
# upwork_info_table = Table(table_name, metadata,
#                           Column('id', Integer, primary_key=True),
#                           Column('raw_data', String(500)),
#                           Column('date_time', DateTime )
#                           )
# metadata.create_all(engine)
# print("table %s created" % table_name)


class UpworkInfo(Base):
    __tablename__ = "upwork_info"
    id = Column(Integer, primary_key=True)
    raw_data = Column(JSON, nullable=False)
    added_time = Column(DateTime, default=datetime.datetime.utcnow)


Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

print("Session is created successful")

Base.metadata.create_all(engine)

print("Table is created successful")

def populate_db(data):
    session.add_all([UpworkInfo(raw_data=json.loads(i)) for i in data])
    session.commit()

