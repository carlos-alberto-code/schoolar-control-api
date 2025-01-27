"""Implementación completa de modelos

Revision ID: 11bf323fbefe
Revises: 8abcf360319f
Create Date: 2025-01-03 23:24:04.571446

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "11bf323fbefe"
down_revision: Union[str, None] = "8abcf360319f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "degrees",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "LENGTH(description) > 3", name="check_degree_description_length"
        ),
        sa.CheckConstraint("LENGTH(name) > 3", name="check_degree_name_length"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "platforms",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("base_url", sa.String(length=255), nullable=True),
        sa.Column("api_config", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("degree_id", sa.Integer(), nullable=False),
        sa.Column("key_registration", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "LENGTH(key_registration) >= 5", name="check_key_registration"
        ),
        sa.ForeignKeyConstraint(
            ["degree_id"],
            ["degrees.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key_registration"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "teachers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("specialization", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "LENGTH(specialization) > 3", name="check_specialization_length"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=False),
        sa.Column("period_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "status IN ('active', 'finished', 'cancelled', 'planned')",
            name="check_course_status",
        ),
        sa.ForeignKeyConstraint(
            ["period_id"],
            ["academic_periods.id"],
        ),
        sa.ForeignKeyConstraint(
            ["teacher_id"],
            ["teachers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "attendance",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "status IN ('present', 'absent', 'late', 'excused')",
            name="check_attendance_status",
        ),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "course_enrollments",
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("enrollment_date", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "status IN ('active', 'dropped', 'completed', 'failed')",
            name="check_enrollment_status",
        ),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
        ),
        sa.PrimaryKeyConstraint("student_id", "course_id"),
    )
    op.create_table(
        "evaluation_components",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("weight", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False),
        sa.Column("platform_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("weight BETWEEN 0 AND 100", name="check_component_weight"),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platforms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "units",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("end_date >= start_date", name="check_unit_dates"),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("unit_id", sa.Integer(), nullable=False),
        sa.Column("component_id", sa.Integer(), nullable=False),
        sa.Column("platform_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("max_score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("weight", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("external_url", sa.String(length=255), nullable=True),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("due_date", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("max_score > 0", name="check_task_score"),
        sa.CheckConstraint("weight BETWEEN 0 AND 100", name="check_task_weight"),
        sa.ForeignKeyConstraint(
            ["component_id"],
            ["evaluation_components.id"],
        ),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platforms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["unit_id"],
            ["units.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("unit_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["unit_id"],
            ["units.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task_submissions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("submission_url", sa.String(length=255), nullable=True),
        sa.Column("submission_text", sa.Text(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "status IN ('draft', 'submitted', 'late', 'graded', 'returned')",
            name="check_submission_status",
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "grades",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("submission_id", sa.Integer(), nullable=False),
        sa.Column("grade", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("graded_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("grade BETWEEN 0 AND 100", name="check_grade_value"),
        sa.ForeignKeyConstraint(
            ["graded_by"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["submission_id"],
            ["task_submissions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.alter_column(
        "academic_periods",
        "name",
        existing_type=mysql.VARCHAR(length=500),
        type_=sa.String(length=255),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "academic_periods",
        "name",
        existing_type=sa.String(length=255),
        type_=mysql.VARCHAR(length=500),
        existing_nullable=False,
    )
    op.drop_table("grades")
    op.drop_table("task_submissions")
    op.drop_table("topics")
    op.drop_table("tasks")
    op.drop_table("units")
    op.drop_table("evaluation_components")
    op.drop_table("course_enrollments")
    op.drop_table("attendance")
    op.drop_table("courses")
    op.drop_table("teachers")
    op.drop_table("students")
    op.drop_table("platforms")
    op.drop_table("degrees")
    # ### end Alembic commands ###
