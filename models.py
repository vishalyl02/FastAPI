from peewee import BooleanField, CharField, ForeignKeyField
from database import BaseModel

class Questions(BaseModel):
    question_text = CharField()

class Choices(BaseModel):
    choice_text = CharField()
    is_correct = BooleanField(default=False)
    question = ForeignKeyField(Questions, backref='choices')
