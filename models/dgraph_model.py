from db.dgraph_client import create_dgraph_client
from datetime import datetime

def set_dgraph_schema(client):
    schema = """
    student_id: string @index(exact) .
    course_id: string @index(exact) .
    instructor_id: string @index(exact) .
    assignment_id: string @index(exact) .
    enrolled: [uid] @reverse .
    teaches: [uid] @reverse .
    assigned_to: [uid] @reverse .
    submitted: [uid] @reverse .
    messaged: [uid] @reverse .
    follows: [uid] @reverse .

    type Student {
        student_id
        enrolled
        messaged
        follows
    }

    type Instructor {
        instructor_id
        teaches
        messaged
    }

    type Course {
        course_id
        assigned_to
    }

    type Assignment {
        assignment_id
        submitted
    }
    """
    client.alter(pydgraph.Operation(schema=schema))

# --- Enroll Student ---
def enroll_student(student_id, course_id):
    client, stub = create_dgraph_client()
    try:
        txn = client.txn()
        data = {
            "uid": f"_:{student_id}",
            "dgraph.type": "Student",
            "student_id": student_id,
            "enrolled": [
                {
                    "uid": f"_:{course_id}",
                    "dgraph.type": "Course",
                    "course_id": course_id
                }
            ]
        }
        response = txn.mutate(set_obj=data, commit_now=True)
        print(f"{student_id} enrolled in {course_id}")
        print("Generated UIDs:", response.uids)
    finally:
        stub.close()

# --- Create Instructor Teaching Relationship ---
def instructor_teaches(instructor_id, course_id):
    client, stub = create_dgraph_client()
    try:
        txn = client.txn()
        data = {
            "uid": f"_:{instructor_id}",
            "dgraph.type": "Instructor",
            "instructor_id": instructor_id,
            "teaches": [
                {
                    "uid": f"_:{course_id}",
                    "dgraph.type": "Course",
                    "course_id": course_id
                }
            ]
        }
        txn.mutate(set_obj=data, commit_now=True)
        print(f"{instructor_id} now teaches {course_id}")
    finally:
        stub.close()

# --- Submit Assignment ---
def submit_assignment(student_id, assignment_id, score):
    client, stub = create_dgraph_client()
    try:
        txn = client.txn()
        data = {
            "uid": f"_:{student_id}",
            "dgraph.type": "Student",
            "student_id": student_id,
            "submitted": [
                {
                    "uid": f"_:{assignment_id}",
                    "dgraph.type": "Assignment",
                    "assignment_id": assignment_id,
                    "score": score
                }
            ]
        }
        response = txn.mutate(set_obj=data, commit_now=True)
        print(f"{student_id} submitted {assignment_id}")
        print("Generated UIDs:", response.uids)
    finally:
        stub.close()

# --- Student Follows Instructor ---
def student_follows_instructor(student_id, instructor_id):
    client, stub = create_dgraph_client()
    try:
        txn = client.txn()
        data = {
            "uid": f"_:{student_id}",
            "dgraph.type": "Student",
            "student_id": student_id,
            "follows": [
                {
                    "uid": f"_:{instructor_id}",
                    "dgraph.type": "Instructor",
                    "instructor_id": instructor_id
                }
            ]
        }
        response = txn.mutate(set_obj=data, commit_now=True)
        print(f"{student_id} now follows {instructor_id}")
        print("Generated UIDs:", response.uids)
    finally:
        stub.close()

# --- Message Between Student and Instructor ---
def message_between_users(sender_id, receiver_id, content):
    client, stub = create_dgraph_client()
    try:
        txn = client.txn()
        data = {
            "uid": f"_:{sender_id}",
            "messaged": [
                {
                    "uid": f"_:{receiver_id}",
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat()
                }
            ]
        }
        txn.mutate(set_obj=data, commit_now=True)
        print(f"{sender_id} messaged {receiver_id}")
    finally:
        stub.close()

# --- Personalized Course Recommendations ---
def recommend_courses(student_id: str, limit: int = 5):
    query = f'''
    {{
      rec(func: eq(student_id, "{student_id}")) @cascade {{
        enrolled {{
          teaches {{
            enrolled(first: {limit}) {{
              course_id
              title
            }}
          }}
        }}
      }}
    }}
    '''
    client, stub = create_dgraph_client()
    try:
        res = client.txn(read_only=True).query(query)
        return res.json
    finally:
        stub.close()

# --- Discussion Forum & Social Interactions ---
def create_forum_post(post_id: str, user_id: str, content: str):
    data = {
      "uid": f"_:{post_id}",
      "dgraph.type": "Post",
      "post_id": post_id,
      "author": [{"uid": f"_:{user_id}"}],
      "content": content,
      "timestamp": datetime.utcnow().isoformat()
    }
    client, stub = create_dgraph_client()
    try:
        client.txn().mutate(set_obj=data, commit_now=True)
    finally:
        stub.close()

def reply_to_post(parent_id: str, reply_id: str, user_id: str, content: str):
    data = {
      "uid": f"_:{parent_id}",
      "replies": [{
        "uid": f"_:{reply_id}",
        "dgraph.type": "Post",
        "post_id": reply_id,
        "author": [{"uid": f"_:{user_id}"}],
        "content": content,
        "timestamp": datetime.utcnow().isoformat()
      }]
    }
    client, stub = create_dgraph_client()
    try:
        client.txn().mutate(set_obj=data, commit_now=True)
    finally:
        stub.close()

# --- Course Prerequisites ---
def add_prerequisite(course_id: str, prereq_id: str):
    data = {
      "uid": f"_:{course_id}",
      "prerequisite": [{"uid": f"_:{prereq_id}"}]
    }
    client, stub = create_dgraph_client()
    try:
        client.txn().mutate(set_obj=data, commit_now=True)
    finally:
        stub.close()

# --- Course Completion Link ---
def mark_course_completed(student_id: str, course_id: str):
    data = {
      "uid": f"_:{student_id}",
      "completed": [{"uid": f"_:{course_id}"}]
    }
    client, stub = create_dgraph_client()
    try:
        client.txn().mutate(set_obj=data, commit_now=True)
    finally:
        stub.close()