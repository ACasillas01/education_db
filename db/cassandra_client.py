from cassandra.cluster import Cluster
import os

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")

def get_cassandra_session():
    cluster = Cluster([CASSANDRA_HOST])
    session = cluster.connect()
    session.set_keyspace("online_edu")
    return session
