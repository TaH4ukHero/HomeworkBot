from sqlalchemy import Column, Integer, String, Date
from data.db_session import SqlAlchemyBase


class History(SqlAlchemyBase):
    __tablename__ = 'HistoryHomework'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)
    date = Column(Date)
    text = Column(String)