from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('postgresql://postgres:567234@195.201.150.230:5433/receipts_db')
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()