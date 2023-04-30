import os
import pytest
from sqlalchemy import MetaData
import sqlalchemy
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

    metadata.create_all(engine, tables=[Metric.__table__])

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(Metric(Name="test1", Label="label1", Value=1))
    session.add(Metric(Name="test1", Label="label2", Value=3))
    session.add(Metric(Name="test1", Label="label2", Value=3))
    session.add(Metric(Name="test2", Label="label3", Value=12))
    session.commit()

    yield
