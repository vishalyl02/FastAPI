from peewee import Model, CharField, BooleanField, ForeignKeyField, PostgresqlDatabase

DATABASE_NAME = 'QuizApplicationYT'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = '12345'
DATABASE_HOST = 'localhost'

db = PostgresqlDatabase(DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST)

class BaseModel(Model):
    class Meta:
        database = db

