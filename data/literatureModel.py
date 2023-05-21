from sqlalchemy import Column, Integer, String, Date
from data.db_session import SqlAlchemyBase


class Literature(SqlAlchemyBase):
    __tablename__ = 'LiteratureHomework'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)
    date = Column(Date)
    text = Column(String)