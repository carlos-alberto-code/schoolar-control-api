from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base


engine = create_engine('sqlite:///schoolar_control.db')


def get_session(): ...
