from db.dgraph_client import create_dgraph_client
import pydgraph

def setup_dgraph_schema():
    client, stub = create_dgraph_client()

    schema = """
    student_id: string @index(exact) .
    instructor_id: string @index(exact) .
    course_id: string @index(exact) .
    assignment_id: string @index(exact) .
    name: string .
    title: string .
    enrolled: [uid] @reverse .
    teaches: [uid] @reverse .
    assigned_to: [uid] @reverse .
    submitted: [uid] @reverse .
    follows: [uid] @reverse .
    messaged: [uid] @reverse .

    type Student {
        student_id
        enrolled
        follows
        messaged
    }

    type Instructor {
        instructor_id
        teaches
        messaged
    }

    type Course {
        course_id
        title
        assigned_to
    }

    type Assignment {
        assignment_id
        submitted
    }
    """

    client.alter(pydgraph.Operation(schema=schema))
    stub.close()
    print("✅ Dgraph schema created.")

if __name__ == "__main__":
    setup_dgraph_schema()
