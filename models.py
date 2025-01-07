from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime, func, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)

    group: Mapped['Group'] = relationship('Group', back_populates='students')
    grades: Mapped[list['Grade']] = relationship('Grade', back_populates='student', cascade="all, delete-orphan")


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    students: Mapped[list["Student"]] = relationship("Student", back_populates="group", cascade="all, delete-orphan")


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    subjects: Mapped[list['Subject']] = relationship('Subject', back_populates='teacher')


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)

    __table_args__ = (
        UniqueConstraint('name', 'teacher_id', name='uq_name_teacher_id'),
    )

    teacher: Mapped['Teacher'] = relationship('Teacher', back_populates="subjects")
    grades: Mapped[list['Grade']] = relationship('Grade', back_populates='subject', cascade="all, delete-orphan")


class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)

    student: Mapped['Student'] = relationship('Student', back_populates='grades')
    subject: Mapped['Subject'] = relationship('Subject', back_populates='grades')
