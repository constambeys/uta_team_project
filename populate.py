import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uta_team_project.settings")

import django

django.setup()

from uta_models.models import *


def populate():
    # INSERT DATA

    create_department("Computing Science")
    create_department("Data Science")
    create_department("Software Engineering")
    create_department("Software Development")
    create_department("Information Security")
    create_department("Information Technology")

    create_course("Internet Technology")
    create_course("Cyber Security")
    create_course("Big Data")
    create_course("Software Engineering")
    create_course("Human Computer Interaction")

    create_lvl_of_study("4th year")
    create_lvl_of_study("MSc")

    create_qualification("Java")
    create_qualification("Python")
    create_qualification("Matlab")
    create_qualification("HTML")
    create_qualification("CSS")
    create_qualification("Javascript")
    create_qualification("SQL")
    create_qualification("UML")

    courses = Course.objects.all()
    departments = Department.objects.all()
    lvls = LevelOfStudy.objects.all()
    instructors = Instructor.objects.all()
    qualifications = Qualification.objects.all()
    students = Student.objects.all()
    requirements = Requirement.objects.all()
    assignments = Assignment.objects.all()
    groups = Group.objects.all()

    create_student("nickozoulis", "Nickolas", "Zoulis", 2211892, departments[0], lvls[1])
    create_student("geo", "Georgia", "Georgiou", 2223979, departments[1], lvls[1])
    create_student("timo", "Timotheos", "Constambeys", 2215104, departments[0], lvls[1])
    create_student("tsveti", "Tsvetelina", "Nikolova", 2199619, departments[5], lvls[1])

    create_instructor("leifos", "Leif", "Azzopardi")
    create_instructor("jozef", "Jozeph", "Maguire")
    create_instructor("rosa", "Rosanne", "English")

    r = create_requirement(1, 2, qualifications[0], qualifications[1])
    a = create_assignment("Assessed Exercise", instructors[0], courses[0], r, students[0], students[1], students[2],
                          students[3])
    create_group("Team UTA", a, students[0], students[1])

    a = create_assignment("Project", instructors[0], courses[0], r, students[0], students[1], students[2],
                          students[3])
    create_group("Team UTA", a, students[0], students[1])

    # PRINT DATA
    for x in departments:
        print "{0}".format(str(x))

    for x in courses:
        print "{0}".format(str(x))

    for x in lvls:
        print "{0}".format(str(x))

    for x in qualifications:
        print "{0}".format(str(x))

    for x in students:
        print "{0}".format(str(x))

    for x in instructors:
        print "{0}".format(str(x))

    for x in requirements:
        print "{0}".format(str(x))

    for x in assignments:
        print "{0}".format(str(x))

    for x in groups:
        print "{0}".format(str(x))


def create_course(name):
    return Course.objects.get_or_create(name=name)[0]


def create_department(name):
    return Department.objects.get_or_create(name=name)[0]


def create_lvl_of_study(lvl):
    LevelOfStudy.objects.get_or_create(lvl=lvl)


def create_student(username, firstname, lastname, matriculation_number, department, lvl):
    (user, created) = User.objects.get_or_create(username=username,
                                                 first_name=firstname,
                                                 last_name=lastname)
    if created:
        user.set_password("1234")
        user.save()
        student = Student(user=user)
        student.matriculationNumber = matriculation_number
        student.department = department
        student.lvlOfStudy = lvl
        student.save()


def create_instructor(username, firstname, lastname):
    (user, created) = User.objects.get_or_create(username=username,
                                                 first_name=firstname,
                                                 last_name=lastname)
    if created:
        user.set_password("1234")
        user.save()
        instructor = Instructor(user=user)
        instructor.save()


def create_qualification(name):
    Qualification.objects.get_or_create(name=name)


def create_assignment(name, instructor, course, requirements, *students):
    (assignment, created) = Assignment.objects.get_or_create(name=name,
                                                             instructor=instructor,
                                                             course=course,
                                                             requirements=requirements)
    if created:
        assignment.save()
        for s in students:
            assignment.students.add(s)
        assignment.save()

    return assignment


def create_group(name, assignment, *students):
    (group, created) = Group.objects.get_or_create(name=name, assignment=assignment)
    # group = Group(name=name, assignment=assignment)
    if created:
        group.save()
        for q in students:
            group.students.add(q)
        group.save()

    return group


def create_requirement(min_group_size, max_group_size, *qualifications):
    (requirement, created) = Requirement.objects.get_or_create(min_group_size=min_group_size,
                                                               max_group_size=max_group_size)

    if created:
        requirement.save()
        for q in qualifications:
            requirement.qualifications.add(q)
        requirement.save()

    return requirement


if __name__ == '__main__':
    print "Starting population script..."
    populate()
