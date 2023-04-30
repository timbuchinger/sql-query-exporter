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

    actual = REGISTRY.get_sample_value("test_query", dict(Name="test1", Label="label1"))
    assert actual == 1.0
    actual = REGISTRY.get_sample_value("test_query", dict(Name="test1", Label="label2"))
    assert actual == 6.0
    actual = REGISTRY.get_sample_value("test_query", dict(Name="test2", Label="label3"))
    assert actual == 12.0
