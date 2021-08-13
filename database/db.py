import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self):
        DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite')
        engine = create_engine(DATABASE_URL, echo=True)

        Session = sessionmaker(bind=engine)
        self.session = Session()
