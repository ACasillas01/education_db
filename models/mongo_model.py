from db.mongo_client import get_mongo_db
from bson.objectid import ObjectId
from datetime import datetime
import bcrypt
import secrets
from datetime import timedelta

db = get_mongo_db()

# --- Users ---
def login_user(email: str, password: str, ip_address: str, device_info: str):
    user = db.users.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode(), user["hashed_password"].encode()):
        return None
    session = {
        "user_id": user["_id"],
        "login_timestamp": datetime.utcnow(),
        "ip_address": ip_address,
        "device_info": device_info,
        "active": True
    }
    session_id = db.sessions.insert_one(session).inserted_id
    return str(session_id)

def find_user_by_email(email):
    return db.users.find_one({"email": email})

def register_user(username, email, password, role):
    if db.users.find_one({"$or": [{"username": username}, {"email": email}]}):
        print("User already exists.")
        return
    
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    user = {
        "username": username,
        "email": email,
        "hashed_password": hashed_pw.decode(),
        "role": role,
        "language_preference": "en",
        "bookmarks": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = db.users.insert_one(user)
    print(f"User {username} registered with ID: {result.inserted_id}")

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
    result = db.courses.insert_one(course)
    print(f"Course '{title}' created with ID: {result.inserted_id}")

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
    result = db.lessons.insert_one(lesson)
    print(f"Lesson '{title}' created with ID: {result.inserted_id}")

# --- Quizzes ---
def create_quiz(course_id, questions):
    quiz = {
        "course_id": ObjectId(course_id),
        "questions": questions,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = db.quizzes.insert_one(quiz)
    print(f"Quiz created with ID: {result.inserted_id}")

# --- Certificates ---
def create_certificate(user_id, course_id, certificate_link):
    cert = {
        "user_id": ObjectId(user_id),
        "course_id": ObjectId(course_id),
        "completion_date": datetime.utcnow(),
        "certificate_link": certificate_link
    }
    result = db.certificates.insert_one(cert)
    print(f"Certificate created with ID: {result.inserted_id}")

# --- Bookmarking Courses ---
def add_bookmark(user_id: str, course_id: str):
    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$addToSet": {"bookmarks": ObjectId(course_id)}}
    )

def remove_bookmark(user_id: str, course_id: str):
    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"bookmarks": ObjectId(course_id)}}
    )

# --- Multi-language Support ---
def set_language_preference(user_id: str, lang_code: str):
    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"language_preference": lang_code, "updated_at": datetime.utcnow()}}
    )

# --- Password Recovery ---
def create_password_reset(email: str):
    user = db.users.find_one({"email": email})
    if not user:
        return None
    token = secrets.token_urlsafe(32)
    db.password_resets.insert_one({
        "user_id": user["_id"],
        "token": token,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(hours=1)
    })
    return token

def reset_password(token: str, new_password: str):
    pr = db.password_resets.find_one({
        "token": token,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    if not pr:
        return False
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    db.users.update_one({"_id": pr["user_id"]}, {"$set": {"hashed_password": hashed}})
    db.password_resets.delete_one({"_id": pr["_id"]})
    return True

# --- Search Courses by Title or Category ---
def search_courses(keyword: str = None, category: str = None):
    q = {}
    if keyword:
        q["$text"] = {"$search": keyword}
    if category:
        q["category"] = category
    cursor = db.courses.find(q)
    if keyword:
        cursor = cursor.sort([("score", {"$meta": "textScore"})])
    return list(cursor)

# --- Course Category Browsing ---
def browse_courses_by_category(category: str):
    return list(db.courses.find({"category": category}))

# --- Logout ---
def logout_user(session_id: str):
    db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"active": False}}
    )

# --- View Course Details
def get_course_details(course_id: str):
    return db.courses.find_one({"_id": ObjectId(course_id)})
