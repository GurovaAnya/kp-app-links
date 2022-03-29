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
    authority = TextField(column_name="authority")
    date = TextField(column_name="date")
    text = TextField(column_name='text')

    class Meta:
        table_name = 'document'
        database = conn


class Link(BaseModel):
    parent_id = ForeignKeyField(column_name="parent_id", model=Document)
    child_id = ForeignKeyField(column_name="child_id", model=Document)
    start_index = IntegerField(column_name="start_index")
    end_index = IntegerField(column_name="end_index")

    class Meta:
        table_name = 'links'


# def initialize_db():
#     conn.connect()
#     conn.create_tables([Document, Link], safe=True)
#     conn.close()





