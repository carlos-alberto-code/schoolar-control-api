from schoolar_control_api.database.models import Student
from schoolar_control_api.database.repository import Repository
from schoolar_control_api.database.connection import get_session


if __name__ == "__main__":

    with get_session() as session:
        student_repo = Repository[Student](Student, session)

        # Get student by ID
        student = student_repo.get(Student.id == 1)

        # Get student by multiple conditions
        student = student_repo.get(
            Student.degree_id == 1, Student.key_registration == "12345"
        )

        # Get all active students in a specific degree
        students = student_repo.get_all(
            Student.deleted_at.is_(None), Student.degree_id == 1
        )

        # Update student
        updated_student = student_repo.update(
            Student.id == 1, values={"key_registration": "54321"}
        )
