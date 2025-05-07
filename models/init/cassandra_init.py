from db.cassandra_client import get_cassandra_session, KEYSPACE
import logging

log = logging.getLogger(__name__)
def setup_cassandra_schema():
    session = get_cassandra_session()

    # Create keyspace if it doesn't exist (optional)
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS online_edu
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    """)

    session.set_keyspace(KEYSPACE)

    # Create tables
    session.execute("""
    CREATE TABLE IF NOT EXISTS user_activity (
        user_id text,
        timestamp timestamp,
        activity_type text,
        metadata map<text, text>,
        PRIMARY KEY (user_id, timestamp)
    ) WITH CLUSTERING ORDER BY (timestamp DESC);
    """)

    session.execute("""
    CREATE TABLE IF NOT EXISTS lesson_completion (
        user_id text,
        lesson_id text,
        course_id text,
        completion_timestamp timestamp,
        quiz_score float,
        PRIMARY KEY (user_id, lesson_id)
    );
    """)

    session.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        user_id text,
        quiz_id text,
        attempt_timestamp timestamp,
        score float,
        responses map<text, text>,
        PRIMARY KEY (user_id, quiz_id)
    );
    """)

    session.execute("""
    CREATE TABLE IF NOT EXISTS session_logs (
        user_id text,
        login_timestamp timestamp,
        logout_timestamp timestamp,
        session_duration int,
        device_info text,
        PRIMARY KEY (user_id, login_timestamp)
    );
    """)

    session.execute("""
    CREATE TABLE IF NOT EXISTS performance_summary (
        user_id text,
        course_id text,
        average_score float,
        lessons_completed int,
        total_lessons int,
        progress_percent float,
        PRIMARY KEY (user_id, course_id)
    );
    """)

    log.info("✅ Cassandra schema setup completed.")
    print("✅ Cassandra keyspace and tables created.")

if __name__ == "__main__":
    setup_cassandra_schema()