from peewee import *

conn = SqliteDatabase('kp.sqlite')

class BaseModel(Model):
    class Meta:
        database = conn


class Document(BaseModel):
    id = AutoField(column_name='id')
    name = TextField(column_name="name")
    type = TextField(column_name="type")
    number = TextField(column_name="number")

    class Meta:
        table_name = 'document'
        database = conn


class Link(BaseModel):
    parent_id = ForeignKeyField(column_name="parent_id", model=Document)
    child_id = ForeignKeyField(column_name="child_id", model=Document)

    class Meta:
        table_name = 'links'


def initialize_db():
    conn.connect()
    conn.create_tables([Document, Link], safe=True)
    add_data()
    conn.close()


def add_data():
    Document(name='Закон 1', type='закон', number='1').save()
    Document(name='Закон 2', type='закон', number='2g').save()

    Link(parent_id='1', child_id='2').save()




