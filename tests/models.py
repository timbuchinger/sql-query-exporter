from sqlalchemy import Column
import sqlalchemy
from sqlalchemy.types import Integer, String

Base = sqlalchemy.orm.declarative_base()


class Metric(Base):
    __tablename__ = "Metric"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255), unique=True, nullable=False)
    value = Column(Integer, nullable=False)
