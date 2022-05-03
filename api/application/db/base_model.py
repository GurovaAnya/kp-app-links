import os

from peewee import *
from playhouse.db_url import connect

link = os.environ['LINKSDB']
conn = connect(link)


class BaseModel(Model):
    class Meta:
        database = conn