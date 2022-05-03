from peewee import AutoField, TextField

from ..db.base_model import BaseModel


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