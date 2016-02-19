import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uta_team_project.settings")

import django

django.setup()

from uta_models.models import *

def populate():
    # Print out what we have added to the user.

    Group.objects.all().delete()
    Assignment.objects.all().delete()

    users = User.objects.all()
    for x in users:
        print "User - {0} -".format(str(x))


    students = Student.objects.all()
    for x in students:
        print "Student - {0} -".format(str(x))

    instructors = Instructor.objects.all()
    for x in instructors:
        print "Instructor - {0} -".format(str(x))

    a = Assignment(instructor=instructors[0], name="Asssignment 1")
    a.save()
    a.students.add(students[0])
    a.save()
    print a

    g = Group(assignment=a, name="Group 1")
    g.save()
    g.students.add(students[0])
    g.save()

    a = Assignment(instructor=instructors[0], name="Asssignment 2")
    a.save()
    a.students.add(students[0])
    a.save()
    print a  # Start execution here!

if __name__ == '__main__':
    print "Starting population script..."
    populate()
