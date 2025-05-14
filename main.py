# main.py - Unified Menu for MongoDB, Cassandra, and Dgraph

from models.mongo_model import (
    register_user, update_user_profile, create_course,
    add_lesson_to_course, create_lesson, create_quiz, create_certificate,
    login_user, logout_user, add_bookmark, remove_bookmark,
    set_language_preference, search_courses, browse_courses_by_category,
    get_course_details, create_password_reset, reset_password
)
from models.cassandra_model import (
    track_lesson_completion, log_quiz_attempt, update_performance_summary,
    get_performance_summary, get_quiz_results, log_session, log_user_activity
)
from models.dgraph_model import (
    enroll_student, instructor_teaches, submit_assignment,
    student_follows_instructor, message_between_users,
    recommend_courses, create_forum_post, reply_to_post,
    add_prerequisite, mark_course_completed
)

from db.cassandra_client import get_cassandra_session
from db.mongo_client import get_mongo_db
from db.dgraph_client import create_dgraph_client
from datetime import datetime


def print_menu():
    options = {
        1: "Register User (MongoDB)",
        2: "Update User Profile (MongoDB)",
        3: "Create Course (MongoDB)",
        4: "Add Lesson to Course (MongoDB)",
        5: "Create Lesson (MongoDB)",
        6: "Create Quiz (MongoDB)",
        7: "Track Lesson Completion (Cassandra)",
        8: "Log Quiz Attempt (Cassandra)",
        9: "Update Performance Summary (Cassandra)",
        10: "Get Performance Summary (Cassandra)",
        11: "Get Quiz Results (Cassandra)",
        12: "Log Session (Cassandra)",
        13: "Enroll Student (Dgraph)",
        14: "Instructor Teaches Course (Dgraph)",
        15: "Submit Assignment (Dgraph)",
        16: "Student Follows Instructor (Dgraph)",
        17: "Message Between Users (Dgraph)",
        18: "Recommend Courses (Dgraph)",
        19: "Create Forum Post (Dgraph)",
        20: "Reply to Forum Post (Dgraph)",
        21: "Add Course Prerequisite (Dgraph)",
        22: "Mark Course Completed (Dgraph)",
        23: "Login (MongoDB)",
        24: "Logout (MongoDB)",
        25: "Bookmark Course (MongoDB)",
        26: "Remove Bookmark (MongoDB)",
        27: "Set Language Preference (MongoDB)",
        28: "Search Courses (MongoDB)",
        29: "Browse Courses by Category (MongoDB)",
        30: "Get Course Details (MongoDB)",
        31: "Create Password Reset Token (MongoDB)",
        32: "Reset Password (MongoDB)",
        33: "Exit"
    }

    print("\n=== Online Education Platform CLI ===")
    for key, value in options.items():
        print(f"{key}. {value}")


def main():
    cass_session = get_cassandra_session()
    mongo_db = get_mongo_db()
    dgraph_client, dgraph_stub = create_dgraph_client()
    while True:
        print_menu()
        choice = int(input("Select an option: "))

        if choice == 1:
            register_user(input("Username: "), input("Email: "), input("Password: "), input("Role: "))
        elif choice == 2:
            update_user_profile(input("User ID: "), input("Name: "), input("Bio: "), input("Photo URL: "))
        elif choice == 3:
            create_course(input("Instructor ID: "), input("Title: "), input("Description: "),
                          input("Category: "), input("Tags (comma-separated): ").split(','))
        elif choice == 4:
            add_lesson_to_course(input("Course ID: "), input("Lesson ID: "))
        elif choice == 5:
            create_lesson(input("Course ID: "), input("Title: "), input("Content: "),
                          input("Content Type: "), input("Resources (comma-separated): ").split(','))
        elif choice == 6:
            create_quiz(input("Course ID: "), [{"question_text": input("Question: "),
                                                 "answer_options": input("Options (comma-separated): ").split(','),
                                                 "correct_answer": input("Correct Answer: ") }])
        elif choice == 7:
            track_lesson_completion(cass_session, input("User ID: "), input("Course ID: "),
                                    input("Lesson ID: "), float(input("Score (or 0): ") or 0))
        elif choice == 8:
            log_quiz_attempt(cass_session, input("User ID: "), input("Quiz ID: "),
                             float(input("Score: ")), {})
        elif choice == 9:
            update_performance_summary(cass_session, input("User ID: "), input("Course ID: "),
                                       float(input("Avg Score: ")), int(input("Lessons Completed: ")),
                                       int(input("Total Lessons: ")))
        elif choice == 10:
            print(get_performance_summary(cass_session, input("User ID: "), input("Course ID: ")))
        elif choice == 11:
            print(get_quiz_results(cass_session, input("User ID: "), input("Quiz ID: ")))
        elif choice == 12:
            log_session(cass_session, input("User ID: "), datetime.utcnow(),
                        datetime.utcnow(), int(input("Duration (min): ")), input("Device Info: "))
        elif choice == 13:
            enroll_student(input("Student ID: "), input("Course ID: "))
        elif choice == 14:
            instructor_teaches(input("Instructor ID: "), input("Course ID: "))
        elif choice == 15:
            submit_assignment(input("Student ID: "), input("Assignment ID: "), float(input("Score: ")))
        elif choice == 16:
            student_follows_instructor(input("Student ID: "), input("Instructor ID: "))
        elif choice == 17:
            message_between_users(input("Sender ID: "), input("Receiver ID: "), input("Content: "))
        elif choice == 18:
            print(recommend_courses(input("Student ID: "), int(input("Limit: "))))
        elif choice == 19:
            create_forum_post(input("Post ID: "), input("User ID: "), input("Content: "))
        elif choice == 20:
            reply_to_post(input("Parent Post ID: "), input("Reply ID: "), input("User ID: "), input("Content: "))
        elif choice == 21:
            add_prerequisite(input("Course ID: "), input("Prereq Course ID: "))
        elif choice == 22:
            mark_course_completed(input("Student ID: "), input("Course ID: "))
        elif choice == 23:
            sid = login_user(input("Email: "), input("Password: "), input("IP: "), input("Device Info: "))
            print(f"Session ID: {sid}")
        elif choice == 24:
            logout_user(input("Session ID: "))
            print("Logged out successfully.")
        elif choice == 25:
            add_bookmark(input("User ID: "), input("Course ID: "))
            print("Course bookmarked.")
        elif choice == 26:
            remove_bookmark(input("User ID: "), input("Course ID: "))
            print("Bookmark removed.")
        elif choice == 27:
            set_language_preference(input("User ID: "), input("Language Code: "))
            print("Language preference updated.")
        elif choice == 28:
            results = search_courses(input("Keyword (leave blank if none): "), input("Category (leave blank if none): "))
            print(results)
        elif choice == 29:
            results = browse_courses_by_category(input("Category: "))
            print(results)
        elif choice == 30:
            print(get_course_details(input("Course ID: ")))
        elif choice == 31:
            token = create_password_reset(input("Email: "))
            print(f"Password reset token: {token}")
        elif choice == 32:
            ok = reset_password(input("Token: "), input("New Password: "))
            print("Password reset successful." if ok else "Password reset failed.")
        elif choice == 33:
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
