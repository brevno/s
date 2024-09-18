from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.config import settings

Base = declarative_base()

class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String, unique=True, index=True)
    hash = Column(String, unique=True, index=True)
    expiration = Column(DateTime)


engine = create_engine(settings.DATABASE_URL, echo=True)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def db_session_default_params():
    # suppress optional parameter in factory, now it won't be requested
    # in a views with db dependency injection
    return db_session()