from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgres://postgres:postgres@localhost:5432/upwork_data")
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))

metadata = MetaData()
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('user_info', String(500))
                    )
metadata.create_all(engine)


class User(object):

    def __init__(self, user_info):
        self.user_info = user_info

mapper(User, users_table)

Session = sessionmaker(bind=engine)
session = Session()


def populate_db(data):
    session.add_all([User(i) for i in data])

session.commit()


