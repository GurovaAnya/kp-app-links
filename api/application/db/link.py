from peewee import ForeignKeyField, IntegerField

from ..db.base_model import BaseModel
from ..db.document import Document


class Link(BaseModel):
    parent_id = ForeignKeyField(column_name="parent_id", model=Document)
    child_id = ForeignKeyField(column_name="child_id", model=Document)
    start_index = IntegerField(column_name="start_index")
    end_index = IntegerField(column_name="end_index")
    type = IntegerField(column_name="type")

    class Meta:
        table_name = 'links'