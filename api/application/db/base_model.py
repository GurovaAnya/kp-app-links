import os

from peewee import *
from playhouse.db_url import connect

from api.application.db.document import Document
from api.application.db.link import Link

link = os.environ['LINKSDB']
conn = connect(link)


class BaseModel(Model):
    class Meta:
        database = conn


def initialize_db():
    conn.connect()
    conn.create_tables([Document, Link], safe=True)
    # add_data()
    conn.close()





