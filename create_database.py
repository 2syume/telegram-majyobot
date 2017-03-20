from sqlalchemy import create_engine

from bot.models import Base
from bot.config import config

if __name__ == "__main__":
    db_connstr = config.get('Database', 'DatabaseUrl')
    engine = create_engine(db_connstr)
    Base.metadata.create_all(engine)
