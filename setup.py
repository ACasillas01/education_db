# bulk_loader.py - Script to insert sample data into MongoDB, Cassandra, and Dgraph

from db.mongo_client import get_mongo_db
from db.cassandra_client import get_cassandra_session
from db.dgraph_client import create_dgraph_client
from datetime import datetime
import pydgraph


# setup_all.py - Setup MongoDB, Cassandra, and Dgraph Models and Sample Data

import subprocess
from models.mongo_init import setup_mongodb_collections
from models.cassandra_init import setup_cassandra_schema
from models.dgraph_init import setup_dgraph_schema

def setup_all():
    print("\n=== Setting up MongoDB Collections and Indexes ===")
    setup_mongodb_collections()

    print("\n=== Setting up Cassandra Keyspace and Tables ===")
    setup_cassandra_schema()

    print("\n=== Setting up Dgraph Schema ===")
    setup_dgraph_schema()

    print("\n=== Loading Sample Data into MongoDB, Cassandra, and Dgraph ===")
    load_mongodb()
    load_cassandra()
    load_dgraph()

    print("\n🚀 Full system setup completed successfully!")

# --- MongoDB ---
def load_mongodb():
    db = get_mongo_db()

    user = {
        "username": "jdoe",
        "email": "jdoe@example.com",
        "hashed_password": "$2b$12$exampleHashedPassword1234567890",
        "profile": {
            "name": "John Doe",
            "bio": "Lifelong learner",
            "photo": "https://cdn.example.com/profiles/jdoe.jpg"
        },
        "language_preference": "en",
        "bookmarks": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    user_id = db.users.insert_one(user).inserted_id

    course = {
        "instructor_id": user_id,
        "title": "Introduction to NoSQL",
        "description": "Explore MongoDB, Cassandra, and Dgraph.",
        "lesson_ids": [],
        "category": "Database",
        "tags": ["NoSQL", "Database", "MongoDB", "Cassandra", "Dgraph"],
        "ratings": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    course_id = db.courses.insert_one(course).inserted_id

    lesson = {
        "course_id": course_id,
        "title": "Lesson 1: What is NoSQL?",
        "content": "<p>NoSQL is...</p>",
        "content_type": "text",
        "resource_urls": ["https://cdn.example.com/courses/lesson1.pdf"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    db.lessons.insert_one(lesson)

    quiz = {
        "course_id": course_id,
        "questions": [
            {
                "question_id": "q1",
                "question_text": "What is MongoDB?",
                "answer_options": ["Relational DB", "NoSQL DB", "File system", "Spreadsheet"],
                "correct_answer": "NoSQL DB"
            }
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    db.quizzes.insert_one(quiz)

    cert = {
        "user_id": user_id,
        "course_id": course_id,
        "completion_date": datetime.utcnow(),
        "certificate_link": "https://cdn.example.com/certificates/cert123.pdf"
    }
    db.certificates.insert_one(cert)

    print("✅ MongoDB sample data inserted.")


# --- Cassandra ---

def load_cassandra():
    session = get_cassandra_session()

    session.execute("""
    INSERT INTO user_activity (user_id, timestamp, activity_type, metadata)
    VALUES ('u123', toTimestamp(now()), 'login', {'ip': '192.168.1.1', 'device': 'Chrome'})
    """)

    session.execute("""
    INSERT INTO lesson_completion (user_id, lesson_id, course_id, completion_timestamp, quiz_score)
    VALUES ('u123', 'l101', 'c101', toTimestamp(now()), 85.0)
    """)

    session.execute("""
    INSERT INTO quiz_attempts (user_id, quiz_id, attempt_timestamp, score, responses)
    VALUES ('u123', 'q101', toTimestamp(now()), 85.0, {'q1': 'NoSQL DB'})
    """)

    session.execute("""
    INSERT INTO session_logs (user_id, login_timestamp, logout_timestamp, session_duration, device_info)
    VALUES ('u123', toTimestamp(now()), toTimestamp(now()), 45, 'Firefox on Linux')
    """)

    session.execute("""
    INSERT INTO performance_summary (user_id, course_id, average_score, lessons_completed, total_lessons, progress_percent)
    VALUES ('u123', 'c101', 88.0, 3, 5, 60.0)
    """)

    print("✅ Cassandra sample data inserted.")


# --- Dgraph ---

def load_dgraph():
    client, stub = create_dgraph_client()
    set_dgraph_schema(client)
    txn = client.txn()

    data = {
        "uid": "_:student123",
        "dgraph.type": "Student",
        "student_id": "u123",
        "enrolled": [
            {
                "uid": "_:course123",
                "dgraph.type": "Course",
                "course_id": "c101",
                "title": "Introduction to NoSQL"
            }
        ],
        "follows": [
            {
                "uid": "_:instructor456",
                "dgraph.type": "Instructor",
                "instructor_id": "i456",
                "name": "Dr. Smith"
            }
        ]
    }

    txn.mutate(set_obj=data, commit_now=True)
    stub.close()
    print("✅ Dgraph sample data inserted.")


def set_dgraph_schema(client):
    schema = """
    student_id: string @index(exact) .
    instructor_id: string @index(exact) .
    course_id: string @index(exact) .
    name: string .
    title: string .
    enrolled: [uid] @reverse .
    follows: [uid] @reverse .
    type Student { student_id enrolled follows }
    type Instructor { instructor_id name }
    type Course { course_id title }
    """
    client.alter(pydgraph.Operation(schema=schema))


# --- Run All ---
if __name__ == '__main__':
    print("\n=== Setting up MongoDB, Cassandra, and Dgraph ===")
    setup_all()

    print("\n=== Loading Sample Data ===")
    load_mongodb()
    load_cassandra()
    load_dgraph()
    print("\n🚀 All sample data loaded successfully.")
