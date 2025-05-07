from db.mongo_client import get_mongo_db
from bson.objectid import ObjectId
from datetime import datetime
import bcrypt

db = get_mongo_db()

# --- Users ---
def find_user_by_email(email):
    return db.users.find_one({"email": email})

def register_user(username, email, password):
    if db.users.find_one({"$or": [{"username": username}, {"email": email}]}):
        print("User already exists.")
        return
    
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    user = {
        "username": username,
        "email": email,
        "hashed_password": hashed_pw.decode(),
        "profile": {},
        "language_preference": "en",
        "bookmarks": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    db.users.insert_one(user)
    print(f"User {username} registered.")

def update_user_profile(user_id, name=None, bio=None, photo=None):
    update = {"updated_at": datetime.utcnow()}
    if name: update["profile.name"] = name
    if bio: update["profile.bio"] = bio
    if photo: update["profile.photo"] = photo
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update})

    # --- Courses ---
def create_course(instructor_id, title, description, category, tags):
    course = {
        "instructor_id": ObjectId(instructor_id),
        "title": title,
        "description": description,
        "lesson_ids": [],
        "category": category,
        "tags": tags,
        "ratings": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    db.courses.insert_one(course)

def add_lesson_to_course(course_id, lesson_id):
    db.courses.update_one({"_id": ObjectId(course_id)}, {"$push": {"lesson_ids": ObjectId(lesson_id)}})

# --- Lessons ---
def create_lesson(course_id, title, content, content_type, resource_urls):
    lesson = {
        "course_id": ObjectId(course_id),
        "title": title,
        "content": content,
        "content_type": content_type,
        "resource_urls": resource_urls,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    db.lessons.insert_one(lesson)

# --- Quizzes ---
def create_quiz(course_id, questions):
    quiz = {
        "course_id": ObjectId(course_id),
        "questions": questions,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    db.quizzes.insert_one(quiz)

# --- Certificates ---
def create_certificate(user_id, course_id, certificate_link):
    cert = {
        "user_id": ObjectId(user_id),
        "course_id": ObjectId(course_id),
        "completion_date": datetime.utcnow(),
        "certificate_link": certificate_link
    }
    db.certificates.insert_one(cert)
