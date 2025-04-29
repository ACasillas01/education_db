from db.mongo_client import get_mongo_db

def setup_mongodb_collections():
    db = get_mongo_db()

    # Users collection
    db.users.create_index([("email", 1)], unique=True)
    db.users.create_index([("username", 1)], unique=True)

    # Sessions collection
    db.sessions.create_index([("user_id", 1)])
    db.sessions.create_index([("user_id", 1), ("login_timestamp", -1)])

    # Password resets
    db.password_resets.create_index([("token", 1)], unique=True)

    # Courses
    db.courses.create_index([("title", "text"), ("description", "text")])
    db.courses.create_index([("category", 1)])
    db.courses.create_index([("tags", 1)])
    db.courses.create_index([("instructor_id", 1)])

    # Lessons
    db.lessons.create_index([("course_id", 1)])

    # Quizzes
    db.quizzes.create_index([("course_id", 1)])

    # Certificates
    db.certificates.create_index([("user_id", 1)])

    print("✅ MongoDB collections and indexes created.")

if __name__ == "__main__":
    setup_mongodb_collections()
