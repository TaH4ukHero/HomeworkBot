from sqlalchemy import Column, Integer, String, Date
from data.db_session import SqlAlchemyBase


class Physics(SqlAlchemyBase):
    __tablename__ = 'PhysicsHomework'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)
    date = Column(Date)
    text = Column(String)