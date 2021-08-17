import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

class Database:
    def __init__(self):
        DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite')
        self.engine = create_engine(f'{DATABASE_URL}?charset=utf8', echo=True)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
