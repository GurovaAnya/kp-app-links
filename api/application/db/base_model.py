import os

from peewee import *
from playhouse.db_url import connect
import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

link = os.environ['LINKSDB']
conn = connect(link)


class BaseModel(Model):
    class Meta:
        database = conn