from datetime import datetime
from cassandra.query import SimpleStatement

# --- Keyspace and Schema Creation ---
def create_keyspace(session, keyspace, replication_factor):
    """
    Create a keyspace in Cassandra if it doesn't already exist.
    """
    session.execute(f"""
    CREATE KEYSPACE IF NOT EXISTS {keyspace}
    WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': {replication_factor}}};
    """)

def create_schema(session):
    """
    Create the necessary tables in the Cassandra keyspace.
    """
    session.execute("""
    CREATE TABLE IF NOT EXISTS user_activity (
        user_id text,
        timestamp timestamp,
        activity_type text,
        metadata map<text, text>,
        PRIMARY KEY (user_id, timestamp)
    ) WITH CLUSTERING ORDER BY (timestamp DESC);
    """)


# --- Lesson Completion Tracking ---
def track_lesson_completion(session, user_id, course_id, lesson_id, score=None):
    query = """
    INSERT INTO lesson_completion (user_id, lesson_id, course_id, completion_timestamp, quiz_score)
    VALUES (%s, %s, %s, %s, %s)
    """
    session.execute(query, (user_id, lesson_id, course_id, datetime.utcnow(), score))
    print(f"Lesson {lesson_id} completed by {user_id}")

# --- User Activity ---
def log_user_activity(session, user_id, activity_type, metadata):
    query = """
    INSERT INTO user_activity (user_id, timestamp, activity_type, metadata)
    VALUES (%s, toTimestamp(now()), %s, %s)
    """
    session.execute(query, (user_id, activity_type, metadata))

# --- Session Logs ---
def log_session(session, user_id, login_timestamp, logout_timestamp, session_duration, device_info):
    query = """
    INSERT INTO session_logs (user_id, login_timestamp, logout_timestamp, session_duration, device_info)
    VALUES (%s, %s, %s, %s, %s)
    """
    session.execute(query, (user_id, login_timestamp, logout_timestamp, session_duration, device_info))

# --- Quiz Attempts ---
def log_quiz_attempt(session, user_id, quiz_id, score, responses):
    query = """
    INSERT INTO quiz_attempts (user_id, quiz_id, attempt_timestamp, score, responses)
    VALUES (%s, %s, toTimestamp(now()), %s, %s)
    """
    session.execute(query, (user_id, quiz_id, score, responses))

# --- Performance Summary ---
def update_performance_summary(session, user_id, course_id, average_score, lessons_completed, total_lessons):
    progress_percent = (lessons_completed / total_lessons) * 100 if total_lessons else 0
    query = """
    INSERT INTO performance_summary (user_id, course_id, average_score, lessons_completed, total_lessons, progress_percent)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    session.execute(query, (user_id, course_id, average_score, lessons_completed, total_lessons, progress_percent))

# --- Student Performance Analytics
def get_performance_summary(session, user_id: str, course_id: str):
    cql = """
    SELECT average_score, lessons_completed, total_lessons, progress_percent
      FROM performance_summary
     WHERE user_id=%s AND course_id=%s;
    """
    stmt = session.prepare(cql)
    row = session.execute(stmt, (user_id, course_id)).one()
    if row:
        return {
            "average_score": row.average_score,
            "lessons_completed": row.lessons_completed,
            "total_lessons": row.total_lessons,
            "progress_percent": row.progress_percent
        }
    return None

# --- Tracking Student Activity ---
def log_user_activity(session, user_id: str, activity_type: str, metadata: dict):
    cql = """
    INSERT INTO user_activity (user_id, timestamp, activity_type, metadata)
    VALUES (%s, toTimestamp(now()), %s, %s)
    """
    stmt = session.prepare(cql)
    session.execute(stmt, (user_id, activity_type, metadata))

# --- Show Quiz Results
def get_quiz_results(session, user_id: str, quiz_id: str):
    cql = """
    SELECT attempt_timestamp, score, responses
      FROM quiz_attempts
     WHERE user_id=%s AND quiz_id=%s;
    """
    stmt = session.prepare(cql)
    return [row._asdict() for row in session.execute(stmt, (user_id, quiz_id))]