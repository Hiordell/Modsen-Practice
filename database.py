import datetime

import sqlalchemy
from sqlalchemy.orm import declarative_base

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
base = declarative_base()


class Documents(base):
    __tablename__ = 'documents'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.TEXT)
    created_date = sqlalchemy.Column(sqlalchemy.DATETIME)
    rubrics = sqlalchemy.Column(sqlalchemy.String(100))
