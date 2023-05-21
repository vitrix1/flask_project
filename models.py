from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func


engine = create_engine("postgresql://app:1234@127.0.0.1:5431/app")
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Ads(Base):
    __tablename__ = "app_ads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    header = Column(String, nullable=False,)
    description = Column(String, nullable=True)
    creation_time = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


Base.metadata.create_all()
