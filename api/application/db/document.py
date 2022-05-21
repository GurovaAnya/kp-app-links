from peewee import AutoField, TextField, IntegerField, DateTimeField

from ..db.base_model import BaseModel


class Document(BaseModel):
    id = AutoField(column_name='id')
    name = TextField(column_name="name")
    type = TextField(column_name="type")
    number = TextField(column_name="number")
    authority = TextField(column_name="authority")
    date = DateTimeField(column_name="date")
    text = TextField(column_name='text')
    ont_id = IntegerField(column_name='ont_id')

    class Meta:
        table_name = 'document'