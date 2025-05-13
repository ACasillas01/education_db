# main.py - Unified Menu for MongoDB, Cassandra, and Dgraph

from models.mongo_model import register_user, update_user_profile, create_course, add_lesson_to_course, create_lesson, create_quiz, create_certificate
from models.cassandra_model import track_lesson_completion, log_user_activity, track_lesson_completion, log_quiz_attempt, log_session, update_performance_summary
from models.dgraph_model import enroll_student, instructor_teaches, submit_assignment, student_follows_instructor, message_between_users
from datetime import datetime


def print_menu():
    options = {
        1: "Register User (MongoDB)",
        2: "Update User Profile (Name, Bio, Photo)(MongoDB)",
        3: "Create Course (MongoDB)",
        4: "Create Lesson & Link to Course(MongoDB)",
        5: "Track Lesson Completion (Cassandra)",
        6: "Create Quiz (MongoDB)",  # New option added
        7: "Log Quiz Attempt (Cassandra)",
        8: "Enroll Student in Course (Dgraph)",
        9: "Instructor Teaches Course (Dgraph)",
        10: "Submit Assignment (Dgraph)",
        11: "Student Follows Instructor (Dgraph)",
        12: "Message Between Users (Dgraph)",
        13: "Exit"
    }
    print("\n=== Online Education Platform CLI ===")
    for key, value in options.items():
        print(f"{key}. {value}")


def main():
    while True:
        print_menu()
        choice = int(input("Select an option: "))

        if choice == 1:
            username = input("Username: ")
            email = input("Email: ")
            password = input("Password: ")
            role = input("Role (student/instructor): ")
            register_user(username, email, password, role)

        elif choice == 2:
            user_id = input("User ID: ")
            name = input("New name: ")
            bio = input("New bio: ")
            photo = input("Photo URL: ")
            update_user_profile(user_id, name, bio, photo)

        elif choice == 3:
            instructor_id = input("Instructor ID: ")
            title = input("Course Title: ")
            desc = input("Description: ")
            cat = input("Category: ")
            tags = input("Tags (comma-separated): ").split(',')
            create_course(instructor_id, title, desc, cat, tags)

        elif choice == 4:
            course_id = input("Course ID: ")
            lesson_id = input("Lesson ID: ")
            create_lesson(course_id, lesson_id)

        elif choice == 5:
            user_id = input("User ID: ")
            course_id = input("Course ID: ")
            lesson_id = input("Lesson ID: ")
            score = float(input("Score (optional, default 0): ") or 0)
            track_lesson_completion(user_id, course_id, lesson_id, score)

        elif choice == 6: 
            course_id = input("Course ID: ")
            num_questions = int(input("Number of questions: "))
            questions = []
            for _ in range(num_questions):
                question_text = input("Question text: ")
                answer_options = input("Answer options (comma-separated): ").split(',')
                correct_answer = input("Correct answer: ")
                questions.append({
                    "question_text": question_text,
                    "answer_options": answer_options,
                    "correct_answer": correct_answer
                })
            create_quiz(course_id, questions)

        elif choice == 7:
            user_id = input("User ID: ")
            quiz_id = input("Quiz ID: ")
            score = float(input("Score: "))
            responses = input("Responses (as key=value pairs comma-separated): ")
            response_dict = dict(item.split('=') for item in responses.split(','))
            log_quiz_attempt(user_id, quiz_id, score, response_dict)

        elif choice == 8:
            student_id = input("Student ID: ")
            course_id = input("Course ID: ")
            enroll_student(student_id, course_id)

        elif choice == 9:
            instructor_id = input("Instructor ID: ")
            course_id = input("Course ID: ")
            instructor_teaches(instructor_id, course_id)

        elif choice == 10:
            student_id = input("Student ID: ")
            assignment_id = input("Assignment ID: ")
            score = float(input("Score: "))
            submit_assignment(student_id, assignment_id, score)

        elif choice == 11:
            student_id = input("Student ID: ")
            instructor_id = input("Instructor ID: ")
            student_follows_instructor(student_id, instructor_id)

        elif choice == 12:
            sender_id = input("Sender ID: ")
            receiver_id = input("Receiver ID: ")
            content = input("Message content: ")
            message_between_users(sender_id, receiver_id, content)


        elif choice == 13:
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
