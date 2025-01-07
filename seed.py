from connect import Session
from models import Student, Group, Teacher, Subject, Grade
from faker import Faker
from faker.providers import DynamicProvider
from sqlalchemy import text

learning_subjects_provider = DynamicProvider(
    provider_name="learning_subject",
    elements=['Mathematics', 'Geometry', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'Computer Science', 'Literature', 'Economics', 'Music', 'Art'],
)
fake = Faker()
fake.add_provider(learning_subjects_provider)


def truncate_tables():
    with Session() as session:
        session.execute(text("TRUNCATE TABLE grades RESTART IDENTITY CASCADE"))
        session.execute(text("TRUNCATE TABLE students RESTART IDENTITY CASCADE"))
        session.execute(text("TRUNCATE TABLE subjects RESTART IDENTITY CASCADE"))
        session.execute(text("TRUNCATE TABLE teachers RESTART IDENTITY CASCADE"))
        session.execute(text("TRUNCATE TABLE groups RESTART IDENTITY CASCADE"))
        session.commit()


def seed_data():
    with Session() as session:

        groups = [Group(name=f"K-{i}") for i in range(1, 4)]
        print(f"Seed {len(groups)} groups.")
        session.commit()
        session.add_all(groups)
        session.commit()

        teachers = [Teacher(name=f"{fake.first_name()} {fake.last_name()}") for _ in range(5)]
        print(f"Seed {len(teachers)} teachers.")
        session.add_all(teachers)
        session.commit()

        subjects = [Subject(name=fake.unique.learning_subject(), teacher_id=fake.random_element(teachers).id) for _ in range(8)]
        print(f"Seed {len(subjects)} subjects.")
        session.add_all(subjects)
        session.commit()

        students = [Student(name=f"{fake.first_name()} {fake.last_name()}", group_id=fake.random_element(groups).id) for _ in range(50)]
        print(f"Seed {len(students)} students.")
        session.add_all(students)
        session.commit()

        for student in students:
            for _ in range(20):
                session.add(Grade(
                    student_id=student.id,
                    subject_id=fake.random_element(subjects).id,
                    grade=fake.random_int(min=60, max=100),
                    created=fake.date_time_between(start_date="-1y", end_date="now"),
                ))
        print(f"Seed {len(students) * 20} grades.")
        session.commit()


if __name__ == "__main__":
    truncate_tables()
    seed_data()
