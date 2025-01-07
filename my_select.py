from connect import Session
from models import Student, Group, Subject, Grade
from sqlalchemy.sql import func, desc


def print_query(query):
    dlm = '-' * 80
    print(f'{dlm}\n{str(query.statement.compile(compile_kwargs={"literal_binds": True}))}\n{dlm}')


def select_1(session):
    query = (session.query(Student.name.label("name"), func.avg(Grade.grade).label("avg"))
             .join(Grade)
             .group_by(Student.id)
             .order_by(desc('avg')).limit(5))
    print_query(query)
    for res in query:
        print(f'{res.name: <20}{res.avg:.2f}')


def select_2(session, subject_id):
    query = (session.query(Student.id, Student.name.label("name"), Subject.name.label("subj"), func.avg(Grade.grade).label("avg"))
             .join(Grade, Student.id == Grade.student_id)
             .join(Subject, Grade.subject_id == Subject.id)
             .filter(Grade.subject_id == subject_id)
             .group_by(Student.id, Subject.name)
             .order_by(desc("avg")))
    print_query(query)
    result = query.first()
    if result:
        print(f"{'Student ID:':<20}{result.id}\n{'Student Name:':<20}{result.name}\n{'Subject:':<20}{result.subj}\n{'Average Grade:':<20}{result.avg:.2f}")
    else:
        print("No students found for the given subject.")


def select_3(session, subject_id):
    query = (session.query(Group.name.label("name"), func.avg(Grade.grade).label("avg"))
             .join(Student, Group.id == Student.group_id)
             .join(Grade, Student.id == Grade.student_id)
             .filter(Grade.subject_id == subject_id)
             .group_by(Group.id)
             .order_by(Group.name))
    print_query(query)
    for res in query:
        print(f'{res.name: <20}{res.avg:.2f}')


def select_4(session):
    query = session.query(func.AVG(Grade.grade).label("avg"))
    print_query(query)
    print(f'{'Average grade:':<20}{query.scalar():.2f}')


def select_5(session, teacher_id):
    query = (session.query(Subject.name.label("name"))
             .filter(Subject.teacher_id == teacher_id)
             .order_by(Subject.name))
    print_query(query)
    for res in query:
        print(res.name)


def select_6(session, group_id):
    query = (session.query(Student.name.label("name"))
             .filter(Student.group_id == group_id)
             .order_by(Student.name))
    print_query(query)
    for res in query:
        print(res.name)


def select_7(session, group_id, subject_id):
    query = (session.query(Student.name, Grade.created, Grade.grade)
             .join(Grade, Student.id == Grade.student_id)
             .filter(Grade.subject_id == subject_id)
             .filter(Student.group_id == group_id)
             .order_by(Student.name, desc(Grade.created)))
    print_query(query)
    for res in query:
        print(f'{res.name:<20}{res.created.strftime('%Y-%m-%d %H:%M'):<20}{res.grade:>6.2f}')


def select_8(session, teacher_id):
    query = (session.query(func.AVG(Grade.grade).label("avg"))
             .join(Subject, Subject.id == Grade.subject_id)
             .filter(Subject.teacher_id == teacher_id))
    print_query(query)
    print(f'{'Average grade:':<20}{query.scalar():.2f}')


def select_9(session, student_id):
    query = (session.query(Subject.name.label("name"))
             .join(Grade, Subject.id == Grade.subject_id)
             .join(Student, Student.id == Grade.student_id)
             .filter(Student.id == student_id)
             .order_by(Subject.name)
             .distinct())
    print_query(query)
    for res in query:
        print(res.name)


def select_10(session, student_id, teacher_id):
    query = (session.query(Subject.name.label("name"))
             .join(Grade, Subject.id == Grade.subject_id)
             .filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
             .order_by(Subject.name)
             .distinct())
    print_query(query)
    for res in query:
        print(res.name)


if __name__ == "__main__":
    with Session() as s:
        print('\n1. Find 5 students with the highest average grades across all subjects')
        select_1(s)
        print('\n2. Find the student with the highest average grade in a specific subject')
        select_2(s, 3)
        print('\n3. Find the average grade in groups for a specific subject')
        select_3(s, 3)
        print('\n4. Find the average grade for the entire stream (across the whole grades table)')
        select_4(s)
        print('\n5. Find which courses are taught by a specific teacher')
        select_5(s, 2)
        print('\n6. Find a list of students in a specific group')
        select_6(s, 2)
        print('\n7. Find the grades of students in a specific group for a specific subject')
        select_7(s, 2, 3)
        print('\n8. Find the average grade given by a specific teacher across their subjects')
        select_8(s, 2)
        print('\n9. Find a list of courses attended by a specific student')
        select_9(s, 25)
        print('\n10. Find a list of courses taught to a specific student by a specific teacher')
        select_10(s, 25, 2)
