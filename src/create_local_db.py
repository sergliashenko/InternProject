from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgres://postgres:postgres@localhost:5432/upwork_data")
if not database_exists(engine.url):
    create_database(engine.url)
    if database_exists(engine.url):
        print("DB is created")
else:
    print("DB Already exist")

metadata = MetaData()
table_name = "upwork_info"
upwork_info_table = Table(table_name, metadata,
                          Column('id', Integer, primary_key=True),
                          Column('raw_data', String(500))
                          )
metadata.create_all(engine)
print("table %s created" % table_name)


class UpworkInfo(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

mapper(UpworkInfo, upwork_info_table)

Session = sessionmaker(bind=engine)
session = Session()
print("Session is created successful")


def populate_db(data):
    session.add_all([UpworkInfo(i) for i in data])
    session.commit()
