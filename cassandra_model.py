from db.cassandra_client import get_cassandra_session
from datetime import datetime

session = get_cassandra_session()

# --- Lesson Completion Tracking ---
def track_lesson_completion(user_id, course_id, lesson_id, score=None):
    query = """
    INSERT INTO lesson_completion (user_id, lesson_id, course_id, completion_timestamp, quiz_score)
    VALUES (%s, %s, %s, %s, %s)
    """
    session.execute(query, (user_id, lesson_id, course_id, datetime.utcnow(), score))
    print(f"Lesson {lesson_id} completed by {user_id}")

    # --- User Activity ---
def log_user_activity(user_id, activity_type, metadata):
    query = """
    INSERT INTO user_activity (user_id, timestamp, activity_type, metadata)
    VALUES (%s, toTimestamp(now()), %s, %s)
    """
    session.execute(query, (user_id, activity_type, metadata))

# --- Session Logs ---
def log_session(user_id, login_timestamp, logout_timestamp, session_duration, device_info):
    query = """
    INSERT INTO session_logs (user_id, login_timestamp, logout_timestamp, session_duration, device_info)
    VALUES (%s, %s, %s, %s, %s)
    """
    session.execute(query, (user_id, login_timestamp, logout_timestamp, session_duration, device_info))

# --- Quiz Attempts ---
def log_quiz_attempt(user_id, quiz_id, score, responses):
    query = """
    INSERT INTO quiz_attempts (user_id, quiz_id, attempt_timestamp, score, responses)
    VALUES (%s, %s, toTimestamp(now()), %s, %s)
    """
    session.execute(query, (user_id, quiz_id, score, responses))

# --- Performance Summary ---
def update_performance_summary(user_id, course_id, average_score, lessons_completed, total_lessons):
    progress_percent = (lessons_completed / total_lessons) * 100 if total_lessons else 0
    query = """
    INSERT INTO performance_summary (user_id, course_id, average_score, lessons_completed, total_lessons, progress_percent)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    session.execute(query, (user_id, course_id, average_score, lessons_completed, total_lessons, progress_percent))

