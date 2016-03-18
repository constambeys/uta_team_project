import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uta_team_project.settings")

import django
from uta_team_project.Matching import Matching

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

    create_rated_qualification("Java", 1)
    create_rated_qualification("Java", 2)
    create_rated_qualification("Java", 3)
    create_rated_qualification("Java", 4)
    create_rated_qualification("SQL", 1)
    create_rated_qualification("SQL", 2)
    create_rated_qualification("SQL", 3)
    create_rated_qualification("SQL", 4)
    create_rated_qualification("HTML", 1)
    create_rated_qualification("HTML", 2)
    create_rated_qualification("HTML", 3)
    create_rated_qualification("HTML", 4)
    create_rated_qualification("Python", 1)
    create_rated_qualification("Python", 2)
    create_rated_qualification("Python", 3)
    create_rated_qualification("Python", 4)
    create_rated_qualification("Matlab", 1)
    create_rated_qualification("Matlab", 2)
    create_rated_qualification("Matlab", 3)
    create_rated_qualification("Matlab", 4)
    create_rated_qualification("Javascript", 1)
    create_rated_qualification("Javascript", 2)
    create_rated_qualification("Javascript", 3)
    create_rated_qualification("Javascript", 4)
    create_rated_qualification("UML", 1)
    create_rated_qualification("UML", 2)
    create_rated_qualification("UML", 3)
    create_rated_qualification("UML", 4)

    courses = Course.objects.all()
    departments = Department.objects.all()
    lvls = LevelOfStudy.objects.all()
    qualifications = Qualification.objects.all()
    rated_qualifications = RatedQualification.objects.all()

    create_student("nickozoulis", "Nickolas", "Zoulis", 2211892, departments[0], lvls[1], rated_qualifications[1],
                   rated_qualifications[5], rated_qualifications[9])
    create_student("geo", "Georgia", "Georgiou", 2223979, departments[1], lvls[1], rated_qualifications[1],
                   rated_qualifications[4], rated_qualifications[12])
    create_student("timo", "Timotheos", "Constambeys", 2215104, departments[0], lvls[1], rated_qualifications[0],
                   rated_qualifications[14], rated_qualifications[8])
    create_student("tsveti", "Tsvetelina", "Nikolova", 2199619, departments[5], lvls[1], rated_qualifications[0],
                   rated_qualifications[4], rated_qualifications[8])
    create_student("natascha", "Natascha", "Harth", 2222222, departments[1], lvls[1], rated_qualifications[14],
                   rated_qualifications[10])

    create_instructor("leifos", "Leif", "Azzopardi")
    create_instructor("jozef", "Jozeph", "Maguire")
    create_instructor("rosa", "Rosanne", "English")

    students = Student.objects.all()
    instructors = Instructor.objects.all()

    r = create_requirement(1, 2, rated_qualifications[1], rated_qualifications[5], rated_qualifications[9])
    a = create_assignment("Assessed Exercise", instructors[0], courses[0], r,[2016, 3, 14, 11, 06, 05], students[0], students[1], students[2],
                          students[3], students[4])

    create_group("Team UTA1", a, students[0], students[1])
    create_group("Team UTA2", a, students[3])
    create_group("Team UTA3", a, students[2], students[3])

    requirements = Requirement.objects.all()
    assignments = Assignment.objects.all()
    groups = Group.objects.all()

    a = create_assignment("Project", instructors[0], courses[0], r, [2016, 3, 23, 11, 06, 05] ,students[0], students[1], students[2],
                          students[3])

    # PRINT DATA
    for x in departments:
        print "{0}".format(str(x))

    for x in courses:
        print "{0}".format(str(x))

    for x in lvls:
        print "{0}".format(str(x))

    for x in qualifications:
        print "{0}".format(str(x))

    for x in rated_qualifications:
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

    # Test Matching
    # ranks = Matching(groups, r, students[4]).rank()
    #
    # print ranks


def create_course(name):
    return Course.objects.get_or_create(name=name)[0]


def create_department(name):
    return Department.objects.get_or_create(name=name)[0]


def create_lvl_of_study(lvl):
    LevelOfStudy.objects.get_or_create(lvl=lvl)


def create_student(username, firstname, lastname, matriculation_number, department, lvl, *rated_qualifications):
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
        for rated_qualif in rated_qualifications:
            student.rated_qualifications.add(rated_qualif)
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


def create_rated_qualification(name, rating):
    qualif = Qualification.objects.get(name=name)
    RatedQualification.objects.get_or_create(qualification=qualif, rating=rating)


def create_assignment(name, instructor, course, requirements, deadline , *students):
    deadline = datetime(deadline[0], deadline[1], deadline[2], deadline[3], deadline[4], deadline[5])
    (assignment, created) = Assignment.objects.get_or_create(name=name,
                                                             instructor=instructor,
                                                             course=course,
                                                             requirements=requirements,
                                                             deadline = deadline)
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


def create_requirement(min_group_size, max_group_size, *rated_qualifications):
    (requirement, created) = Requirement.objects.get_or_create(min_group_size=min_group_size,
                                                               max_group_size=max_group_size)

    if created:
        requirement.save()
        for q in rated_qualifications:
            requirement.rated_qualifications.add(q)
        requirement.save()

    return requirement


if __name__ == '__main__':
    print "Starting population script..."
    populate()
    
