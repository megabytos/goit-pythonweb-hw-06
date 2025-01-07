from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from settings import url_to_db

engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()
