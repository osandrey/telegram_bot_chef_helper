from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text, func
from .postgres_conn import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)
    created_date = Column(Date, default=func.now())
    active = Column(Boolean, default=True)
    language = Column(String(10), default='en')



class Receipt(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    instructions = Column(Text, nullable=False)
    image = Column(String(200), nullable=False)
    created_date = Column(Date, default=func.now())
    update_date = Column(Date, default=func.now(), onupdate=func.now())
    reviews = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='receipts')



