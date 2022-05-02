from peewee import ForeignKeyField, IntegerField

from api.application.db.base_model import BaseModel
from api.application.db.document import Document


class Link(BaseModel):
    parent_id = ForeignKeyField(column_name="parent_id", model=Document)
    child_id = ForeignKeyField(column_name="child_id", model=Document)
    start_index = IntegerField(column_name="start_index")
    end_index = IntegerField(column_name="end_index")

    class Meta:
        table_name = 'links'