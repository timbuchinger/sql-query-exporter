import os
import sqlalchemy
import yaml
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily
from models import *
from project.models import *
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

config_file = os.getenv("SQL_QUERY_EXPORTER_CONFIG_PATH", "config.yaml")


class CustomCollector(object):
    def __init__(self, config):
        self.config = config

    def collect(self):
        for connection in config.connections:
            engine = sqlalchemy.create_engine(connection.connection_string)
            Session = sessionmaker(engine)
            with Session() as session:
                for query in connection.queries:
                    print(query.name)
                    print(query.query)
                    print(query.label_columns)

                    result = session.execute(text(query.query)).fetchall()
                    print(result)

                    for row in result:
                        if query.metric_type.lower() == "gauge":
                            yield GaugeMetricFamily(
                                query.name,
                                query.help_text,
                                value=row._mapping[query.value_column],
                            )
                        elif query.metric_type.lower() == "counter":
                            pass
                            # c = CounterMetricFamily("my_counter_total", "Help text", labels=["foo"])
                            # c.add_metric(["bar"], 1.7)
                            # c.add_metric(["baz"], 3.8)
                            # yield c


with open(config_file, mode="rb") as file:
    raw = yaml.safe_load(file)
    print(raw)
    connections = []
    for connection in raw["connections"]:
        print(connection["name"])
        queries = []
        for query in connection["queries"]:
            queries.append(
                Query(
                    query["name"],
                    query["type"],
                    query["helpText"],
                    query["query"],
                    query["labelColumns"],
                )
            )
            print(query["name"])
            print(query["query"])
        connections.append(
            Connection(connection["name"], connection["connectionString"], queries)
        )

    global config
    config = Config(connections)


print(config)


REGISTRY.register(CustomCollector(config))
server = start_http_server(8000)
# start_http_server(8080, registry=self.registry)

if __name__ == "__main__":
    input("Press Enter to exit...")
