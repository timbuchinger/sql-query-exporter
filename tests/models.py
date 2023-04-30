from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from conftest import Base


class Metric(Base):
    __tablename__ = "Metric"

    ID = Column(Integer, primary_key=True, autoincrement="auto")
    Name = Column(String(255), nullable=False)
    Label = Column(String(255), nullable=False)
    Value = Column(Integer, nullable=False)
