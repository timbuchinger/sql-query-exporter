import sqlalchemy as db


class Config:
    connections = []

    def __init__(self, connections):
        self.connections = connections


class Connection:
    name = ""
    connection_string = ""
    queries = []

    def __init__(self, name, connection_string, queries):
        self.name = name
        self.connection_string = connection_string
        self.queries = queries
        self.engine = db.create_engine(connection_string, echo=True)


class Query:
    name = ""
    metric_type = ""
    help_text = ""
    query = ""
    label_columns = []
    value_column = "Total"

    def __init__(self, name, metric_type, help_text, query, label_columns):
        self.name = name
        self.metric_type = metric_type
        self.help_text = help_text
        self.query = query
        self.label_columns.append(label_columns)
