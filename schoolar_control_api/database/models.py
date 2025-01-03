from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, Column, Table, DATE, TIMESTAMP, TIME, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        CheckConstraint('LENGTH(name) > 3', name='check_role_name_length')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped['User'] = relationship('User', secondary='roles_users', back_populates='roles')

    def __repr__(self):
        return f'Role(id={self.id!r}, name={self.name!r})'


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint('LENGTH(username) > 3', name='check_username_length'),
        CheckConstraint('LENGTH(password) > 6', name='check_password_length'),
        CheckConstraint(r"email ~* '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'", name='check_email_format')
    )


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)

    roles: Mapped[Role] = relationship('Role', secondary='roles_users', back_populates='users')

    def __repr__(self):
        return f'User(id={self.id!r}, fullname={self.fullname!r}, username={self.username!r}, email={self.email!r})'


roles_users = Table(
    'roles_users',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
)

