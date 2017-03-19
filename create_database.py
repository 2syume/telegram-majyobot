from sqlalchemy import create_engine

from bot.models import Base
from config import Config

if __name__ == "__main__":
    engine = create_engine(Config.DATABASE_CONNECTION)
    Base.metadata.create_all(engine)
