from datetime import date, datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Integer,
    Numeric,
    String,
    ForeignKey,
    Column,
    Table,
    CheckConstraint,
    Text,
)


class Base(DeclarativeBase):
    """Clase base para todos los modelos."""

    pass


class Role(Base):
    """Modelo que representa un rol en el sistema."""

    __tablename__ = "roles"
    __table_args__ = (
        CheckConstraint("LENGTH(name) > 3", name="check_role_name_length"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped["User"] = relationship(
        "User", secondary="roles_users", back_populates="roles"
    )

    def __repr__(self):
        return f"Role(id={self.id!r}, name={self.name!r})"


class User(Base):
    """Modelo que representa un usuario en el sistema."""

    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("LENGTH(username) > 3", name="check_username_length"),
        CheckConstraint("LENGTH(password) > 6", name="check_password_length"),
        CheckConstraint(
            r"email REGEXP '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'",
            name="check_email_format",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)

    roles: Mapped[Role] = relationship(
        "Role", secondary="roles_users", back_populates="users"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, fullname={self.fullname!r}, username={self.username!r}, email={self.email!r})"


roles_users = Table(
    "roles_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)


class Degree(Base):
    """Modelo que representa un grado académico en el sistema."""

    __tablename__ = "degrees"
    __table_args__ = (
        CheckConstraint("LENGTH(name) > 3", name="check_degree_name_length"),
        CheckConstraint(
            "LENGTH(description) > 3", name="check_degree_description_length"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    students: Mapped[List["Student"]] = relationship(back_populates="degree")

    def __repr__(self) -> str:
        return f"Degree(id={self.id!r}, name={self.name!r})"


class AcademicPeriod(Base):
    """Modelo que representa un periodo académico en el sistema."""

    __tablename__ = "academic_periods"
    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="check_period_dates"),
        CheckConstraint(
            "status IN ('active', 'finished', 'cancelled', 'planned')",
            name="check_period_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    courses: Mapped[List["Course"]] = relationship(back_populates="period")

    def __repr__(self) -> str:
        return f"AcademicPeriod(id={self.id!r}, name={self.name!r}, status={self.status!r})"


class Teacher(Base):
    """Modelo que representa un profesor en el sistema."""

    __tablename__ = "teachers"
    __table_args__ = (
        CheckConstraint(
            "LENGTH(specialization) > 3", name="check_specialization_length"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )
    specialization: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped[User] = relationship(foreign_keys=[user_id])
    courses: Mapped[List["Course"]] = relationship(back_populates="teacher")

    def __repr__(self) -> str:
        return f"Teacher(id={self.id!r}, user_id={self.user_id!r})"


class Student(Base):
    """Modelo que representa un estudiante en el sistema."""

    __tablename__ = "students"
    __table_args__ = (
        CheckConstraint("LENGTH(key_registration) >= 5", name="check_key_registration"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )
    degree_id: Mapped[int] = mapped_column(ForeignKey("degrees.id"), nullable=False)
    key_registration: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped[User] = relationship(foreign_keys=[user_id])
    degree: Mapped[Degree] = relationship(back_populates="students")
    enrollments: Mapped[List["CourseEnrollment"]] = relationship(
        back_populates="student"
    )
    submissions: Mapped[List["TaskSubmission"]] = relationship(back_populates="student")
    attendance_records: Mapped[List["Attendance"]] = relationship(
        back_populates="student"
    )

    def __repr__(self) -> str:
        return f"Student(id={self.id!r}, user_id={self.user_id!r}, key_registration={self.key_registration!r})"


class Course(Base):
    """Modelo que representa un curso en el sistema."""

    __tablename__ = "courses"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'finished', 'cancelled', 'planned')",
            name="check_course_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    period_id: Mapped[int] = mapped_column(
        ForeignKey("academic_periods.id"), nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    teacher: Mapped[Teacher] = relationship(back_populates="courses")
    period: Mapped[AcademicPeriod] = relationship(back_populates="courses")
    enrollments: Mapped[List["CourseEnrollment"]] = relationship(
        back_populates="course"
    )
    units: Mapped[List["Unit"]] = relationship(
        back_populates="course", order_by="Unit.order_index"
    )
    evaluation_components: Mapped[List["EvaluationComponent"]] = relationship(
        back_populates="course"
    )
    tasks: Mapped[List["Task"]] = relationship(back_populates="course")
    attendance_records: Mapped[List["Attendance"]] = relationship(
        back_populates="course"
    )

    def __repr__(self) -> str:
        return f"Course(id={self.id!r}, code={self.code!r}, name={self.name!r})"


class CourseEnrollment(Base):
    """Modelo que representa la inscripción de un estudiante en un curso."""

    __tablename__ = "course_enrollments"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'dropped', 'completed', 'failed')",
            name="check_enrollment_status",
        ),
    )

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    enrollment_date: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    student: Mapped[Student] = relationship(back_populates="enrollments")
    course: Mapped[Course] = relationship(back_populates="enrollments")

    def __repr__(self) -> str:
        return f"CourseEnrollment(student_id={self.student_id!r}, course_id={self.course_id!r}, status={self.status!r})"


class Unit(Base):
    """Modelo que representa una unidad dentro de un curso."""

    __tablename__ = "units"
    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="check_unit_dates"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    course: Mapped[Course] = relationship(back_populates="units")
    topics: Mapped[List["Topic"]] = relationship(
        back_populates="unit", order_by="Topic.order_index"
    )
    tasks: Mapped[List["Task"]] = relationship(back_populates="unit")

    def __repr__(self) -> str:
        return f"Unit(id={self.id!r}, name={self.name!r}, order_index={self.order_index!r})"


class Topic(Base):
    """Modelo que representa un tema dentro de una unidad."""

    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    unit: Mapped[Unit] = relationship(back_populates="topics")

    def __repr__(self) -> str:
        return f"Topic(id={self.id!r}, name={self.name!r}, order_index={self.order_index!r})"


class Platform(Base):
    """Modelo que representa una plataforma externa utilizada en el sistema."""

    __tablename__ = "platforms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    base_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    api_config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    components: Mapped[List["EvaluationComponent"]] = relationship(
        back_populates="platform"
    )
    tasks: Mapped[List["Task"]] = relationship(back_populates="platform")

    def __repr__(self) -> str:
        return f"Platform(id={self.id!r}, name={self.name!r}, is_active={self.is_active!r})"


class EvaluationComponent(Base):
    """Modelo que representa un componente de evaluación en el sistema."""

    __tablename__ = "evaluation_components"
    __table_args__ = (
        CheckConstraint("weight BETWEEN 0 AND 100", name="check_component_weight"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    platform_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("platforms.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    course: Mapped[Course] = relationship(back_populates="evaluation_components")
    platform: Mapped[Optional[Platform]] = relationship(back_populates="components")
    tasks: Mapped[List["Task"]] = relationship(back_populates="component")

    def __repr__(self) -> str:
        return f"EvaluationComponent(id={self.id!r}, name={self.name!r}, weight={self.weight!r})"


class Task(Base):
    """Modelo que representa una tarea asignada a los estudiantes."""

    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("max_score > 0", name="check_task_score"),
        CheckConstraint("weight BETWEEN 0 AND 100", name="check_task_weight"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    component_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_components.id"), nullable=False
    )
    platform_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("platforms.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    max_score: Mapped[float] = mapped_column(
        Numeric(5, 2), default=100.00, nullable=False
    )
    weight: Mapped[float] = mapped_column(Numeric(5, 2), default=1.00, nullable=False)
    external_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    course: Mapped[Course] = relationship(back_populates="tasks")
    unit: Mapped[Unit] = relationship(back_populates="tasks")
    component: Mapped[EvaluationComponent] = relationship(back_populates="tasks")
    platform: Mapped[Optional[Platform]] = relationship(back_populates="tasks")
    submissions: Mapped[List["TaskSubmission"]] = relationship(back_populates="task")

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r}, due_date={self.due_date!r})"


class TaskSubmission(Base):
    """Modelo que representa la entrega de una tarea por parte de un estudiante."""

    __tablename__ = "task_submissions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'submitted', 'late', 'graded', 'returned')",
            name="check_submission_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    submission_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    submission_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    status: Mapped[str] = mapped_column(String(50), default="submitted", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    task: Mapped[Task] = relationship(back_populates="submissions")
    student: Mapped[Student] = relationship(back_populates="submissions")
    grade: Mapped[Optional["Grade"]] = relationship(
        back_populates="submission", uselist=False
    )

    def __repr__(self) -> str:
        return f"TaskSubmission(id={self.id!r}, task_id={self.task_id!r}, status={self.status!r})"


class Grade(Base):
    """Modelo que representa la calificación de una tarea."""

    __tablename__ = "grades"
    __table_args__ = (
        CheckConstraint("grade BETWEEN 0 AND 100", name="check_grade_value"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("task_submissions.id"), nullable=False
    )
    grade: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    graded_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    submission: Mapped[TaskSubmission] = relationship(back_populates="grade")
    grader: Mapped[User] = relationship(foreign_keys=[graded_by])

    def __repr__(self) -> str:
        return f"Grade(id={self.id!r}, submission_id={self.submission_id!r}, grade={self.grade!r})"


class Attendance(Base):
    """Modelo que representa el registro de asistencia de un estudiante en un curso."""

    __tablename__ = "attendance"
    __table_args__ = (
        CheckConstraint(
            "status IN ('present', 'absent', 'late', 'excused')",
            name="check_attendance_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="present", nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    course: Mapped[Course] = relationship(back_populates="attendance_records")
    student: Mapped[Student] = relationship(back_populates="attendance_records")

    def __repr__(self) -> str:
        return f"Attendance(id={self.id!r}, student_id={self.student_id!r}, status={self.status!r})"
