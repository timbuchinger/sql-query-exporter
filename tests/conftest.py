import os
import pytest
from sqlalchemy import MetaData, Table
from sqlalchemy import Column
import sqlalchemy
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker


engine = None
Base = sqlalchemy.orm.declarative_base()


@pytest.fixture(scope="module")
def init_database():
    from tests.models import Metric

    os.environ["SQL_QUERY_EXPORTER_CONFIG_PATH"] = "tests/test_config.yaml"

    engine = sqlalchemy.create_engine("sqlite:///test.db")
    metadata = MetaData()
    exist = sqlalchemy.inspect(engine).has_table("Metric")
    if exist == True:
        Metric.__table__.drop(engine)

    Table(
        "Metric",
        metadata,
        Column("id", Integer(), primary_key=True),
        Column("name", String(200), nullable=False),
        Column("value", Integer()),
    )
    metadata.create_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(Metric(name="test", value=1))
    session.add(Metric(name="test", value=3))
    session.add(Metric(name="test2", value=12))
    session.commit()

    yield
