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

    create_rated_qualification("Java", 1) #0
    create_rated_qualification("Java", 2) #1
    create_rated_qualification("Java", 3) #2
    create_rated_qualification("Java", 4) #3
    create_rated_qualification("SQL", 1) #4
    create_rated_qualification("SQL", 2) #5
    create_rated_qualification("SQL", 3) #6
    create_rated_qualification("SQL", 4) #7
    create_rated_qualification("HTML", 1) #8
    create_rated_qualification("HTML", 2) #9
    create_rated_qualification("HTML", 3) #10
    create_rated_qualification("HTML", 4) #11
    create_rated_qualification("Python", 1) #12
    create_rated_qualification("Python", 2) #13
    create_rated_qualification("Python", 3) #14
    create_rated_qualification("Python", 4) #15
    create_rated_qualification("Matlab", 1) #16
    create_rated_qualification("Matlab", 2) #17
    create_rated_qualification("Matlab", 3) #18
    create_rated_qualification("Matlab", 4) #19
    create_rated_qualification("Javascript", 1) #20
    create_rated_qualification("Javascript", 2) #21
    create_rated_qualification("Javascript", 3) #22
    create_rated_qualification("Javascript", 4) #23
    create_rated_qualification("UML", 1) #24
    create_rated_qualification("UML", 2) #25
    create_rated_qualification("UML", 3) #26
    create_rated_qualification("UML", 4) #27

    courses = Course.objects.all()
    departments = Department.objects.all()
    lvls = LevelOfStudy.objects.all()
    qualifications = Qualification.objects.all()
    rated_qualifications = RatedQualification.objects.all()

    create_student_fixed("laura", "Laura", "Laur", 2211890, departments[0], lvls[1], "laura",  rated_qualifications[1],
                   rated_qualifications[5], rated_qualifications[13],rated_qualifications[18],
                   rated_qualifications[25])
    create_student_fixed("david", "David", "davi", 2211896, departments[0], lvls[1], "david", rated_qualifications[0],
                   rated_qualifications[6], rated_qualifications[15],rated_qualifications[20],
                   rated_qualifications[26])
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
    create_student("james", "James", "Kirin", 2232456, departments[3], lvls[0], rated_qualifications[3],
                   rated_qualifications[5], rated_qualifications[11], rated_qualifications[12],
                   rated_qualifications[24], rated_qualifications[20],rated_qualifications[16])
    create_student("nathalie", "Nathalie", "Dixie", 2385698, departments[3], lvls[0], rated_qualifications[1],
                   rated_qualifications[7],rated_qualifications[9],rated_qualifications[12],
                   rated_qualifications[17],rated_qualifications[20],rated_qualifications[25])
    create_student("maria", "Maria", "Hollon", 2381222, departments[4], lvls[1], rated_qualifications[2],
                   rated_qualifications[6],rated_qualifications[11],rated_qualifications[13],
                   rated_qualifications[16],rated_qualifications[22],rated_qualifications[27])
    create_student("jarend", "Jare", "Jinks", 2341222, departments[2], lvls[1], rated_qualifications[0],
                   rated_qualifications[5],rated_qualifications[8],rated_qualifications[14],
                   rated_qualifications[17],rated_qualifications[20],rated_qualifications[26])
    create_student("kouri", "Kiter", "Zile", 2344221, departments[4], lvls[0], rated_qualifications[25],
                   rated_qualifications[5])
    create_student("dixie", "Direl", "Adri", 2264221, departments[3], lvls[1], rated_qualifications[23],
                   rated_qualifications[1])
    create_student("doing", "Dude", "Dudie", 2264121, departments[2], lvls[0], rated_qualifications[22])
    #12
    create_student("cailitin", "Caitlin", "Jinx", 2262921, departments[3], lvls[0], rated_qualifications[2])
    create_student("heim", "Heimerdinger", "Scin", 2262931, departments[2], lvls[1], rated_qualifications[3], rated_qualifications[7],
                   rated_qualifications[15], rated_qualifications[23])
    create_student("teemo", "Tim", "Frine", 2452921, departments[1], lvls[1], rated_qualifications[4], rated_qualifications[10],
                   rated_qualifications[16], rated_qualifications[22])
    create_student("ashe", "Ashley", "Troll", 2234921, departments[4], lvls[0], rated_qualifications[2], rated_qualifications[12],
                   rated_qualifications[18], rated_qualifications[23])
    create_student("volli", "Vollie", "Beart", 2234920, departments[2], lvls[0], rated_qualifications[1], rated_qualifications[7],
                   rated_qualifications[15], rated_qualifications[23])
    create_student("marina", "Marina", "Sulok", 2234970, departments[2], lvls[1], rated_qualifications[6], rated_qualifications[11],
                   rated_qualifications[17], rated_qualifications[24])
    create_student("karen", "Karen", "Stilk", 4334970, departments[1], lvls[1], rated_qualifications[6], rated_qualifications[11],
                   rated_qualifications[17], rated_qualifications[24])
    create_student("kirki", "Kirk", "Stalon", 4334932, departments[4], lvls[1], rated_qualifications[5], rated_qualifications[23],
                   rated_qualifications[11], rated_qualifications[16])
    create_student("simon", "Simone", "Stanler", 4335432, departments[2], lvls[0], rated_qualifications[4], rated_qualifications[22],
                   rated_qualifications[11], rated_qualifications[17])
    create_student("silia", "Silia", "Staper", 4335402, departments[2], lvls[0], rated_qualifications[4], rated_qualifications[22],
                   rated_qualifications[11], rated_qualifications[17])
    create_student("stan", "Stanley", "Stegher", 4333402, departments[2], lvls[0], rated_qualifications[4], rated_qualifications[22],
                   rated_qualifications[11], rated_qualifications[17])
    #21
    create_instructor_fixed("leifos", "Leif", "Azzopardi","leifos")
    create_instructor("jozef", "Jozeph", "Maguire")
    create_instructor("rosa", "Rosanne", "English")

    students = Student.objects.all()
    instructors = Instructor.objects.all()

    r = create_requirement(1, 4, rated_qualifications[1], rated_qualifications[5], rated_qualifications[9])
    a = create_assignment("Assessed Exercise 1", instructors[0], courses[0], r,[2016, 3, 25, 11, 06, 05], students[0], students[1], students[2],
                          students[3], students[4],students[5], students[6], students[7],
                          students[8], students[9],students[10],students[11],students[12],
                          students[13],students[14],students[15],students[16],students[17],
                          students[18],students[19],students[20],students[21])
    b = create_assignment("Assessed Exercise 2", instructors[0], courses[0], r,[2016, 3, 29, 11, 06, 05], students[0], students[1], students[2],
                          students[3], students[4],students[5], students[6], students[7],
                          students[8], students[9],students[10],students[11],students[12],
                          students[13],students[14],students[15],students[16],students[17],
                          students[18],students[19],students[20],students[21])
    c = create_assignment("Assessed Exercise 3", instructors[0], courses[0], r,[2016, 3, 30, 11, 06, 05], students[0], students[1], students[2],
                          students[3], students[4],students[5], students[6], students[7],
                          students[8], students[9],students[10],students[11],students[12],
                          students[13],students[14],students[15],students[16],students[17],
                          students[18],students[19],students[20],students[21])

    create_group("Team UTaaa", a, students[15], students[16])
    create_group("Team geeks", a, students[17])
    create_group("Team dudes", a, students[2], students[4])
    create_group("Team dudies", a, students[5], students[6], students[7], students[8])
    create_group("Team DA", a, students[9], students[10])
    create_group("Team Nevis", a, students[11], students[12])
    create_group("Team Glasgow", a, students[13], students[14])
    create_group("Team Glasgow", b, students[13], students[14])
    create_group("Team Glasgow", c, students[13], students[14])

    requirements = Requirement.objects.all()
    assignments = Assignment.objects.all()
    groups = Group.objects.all()


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


def create_student_fixed(username, firstname, lastname, matriculation_number, department, lvl,fixedpass, *rated_qualifications):
    (user, created) = User.objects.get_or_create(username=username,
                                                 first_name=firstname,
                                                 last_name=lastname)
    if created:
        user.set_password(fixedpass)
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


def create_instructor_fixed(username, firstname, lastname,fixedpass):
    (user, created) = User.objects.get_or_create(username=username,
                                                 first_name=firstname,
                                                 last_name=lastname)
    if created:
        user.set_password(fixedpass)
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
    
