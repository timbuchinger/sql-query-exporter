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
    Metric.__table__.drop(engine)

    exist = sqlalchemy.inspect(engine).has_table("Metrics")
    if exist == False:
        print("=Table doesn't exist=")
        metrics = Table(
            "Metric",
            metadata,
            Column("id", Integer(), primary_key=True),
            Column("name", String(200), nullable=False),
            Column("value", Integer()),
        )
        metadata.create_all(engine)
        print("=Table was created=")

    Base.metadata.create_all(engine)
    # sa.create_all()

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(Metric(name="test", value=1))
    session.add(Metric(name="test", value=3))
    session.add(Metric(name="test2", value=12))
    session.commit()

    yield

    # sqlalchemy.drop_all()
