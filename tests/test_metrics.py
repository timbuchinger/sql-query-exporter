"""
Test the metrics
"""
import os
from prometheus_client import REGISTRY

os.environ["SQL_QUERY_EXPORTER_CONFIG_PATH"] = "test_config.yaml"


def test_metrics(init_database):
    """
    GIVEN
    WHEN
    THEN
    """
    import project.main

    test = REGISTRY.get_sample_value("test_query")  # , dict(Name="test"))
    assert test == 4
    # test2 = REGISTRY.get_sample_value("test_query"), dict(Name="test2"))
    # assert test2 == 12
