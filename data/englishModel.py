from sqlalchemy import Column, Integer, String, Date
from data.db_session import SqlAlchemyBase


class English(SqlAlchemyBase):
    __tablename__ = 'EnglishHomework'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)
    date = Column(Date)
    text = Column(String)