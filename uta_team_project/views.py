from django.http import *
from django.contrib.auth import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from forms import *
from uta_auth.forms import UserForm, StudentForm, UserUpdateForm, StudentUpdateForm, InstructorUpdateForm
from uta_models.models import Student
from django.utils.safestring import mark_safe
import calendar
from datetime import date
from MyCalendar import MyCalendar
from Matching import Matching



def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:

                return HttpResponse("Your Rango account is disabled.")
        else:

            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponseRedirect(reverse('error', kwargs={'message': "Invalid login details"}))
    else:
        return render(request, 'index.html', {})


def error(request, message):
    context_dict = {}
    context_dict['message'] = message
    return render(request, 'error.html', context_dict)


@login_required
def home(request):
    if request.user.is_authenticated():
        if hasattr(request.user, 'student'):
            return student_home(request)
        elif hasattr(request.user, 'instructor'):
            return instructor_home(request)
        else:
            logout(request)  # Clear store session
            return HttpResponse("Oops something went wrong!!")
    else:
        return HttpResponse("Not logged in!")


@login_required
def find_team(request, assignment_id):
    student = request.user.student
    my_group = student.group_set.filter(assignment_id=assignment_id)
    if my_group.count() != 0:
        return HttpResponse("Sorry you are already in a group")

    context_dict = {}
    # The assignment that the user has selected
    assignment = Assignment.objects.get(id=assignment_id)
    requirements = assignment.requirements
    groups = Group.objects.filter(assignment__name=assignment.name)

    groups_benefits = Matching(groups, requirements, student).rank()
    ranked_groups = [g for (g, b) in groups_benefits]

    # print ranked_groups

    context_dict['ranked_groups'] = ranked_groups
    if len(ranked_groups) > 0:
        context_dict['top_group'] = ranked_groups[0]
    context_dict['assignment'] = assignment
    context_dict['username'] = request.user.username
    return render(request, 'find_team.html', context_dict)


@login_required
def select_team(request, team_id):
    if request.user.is_authenticated():
        if hasattr(request.user, 'student'):
            team = Group.objects.get(pk=team_id)

            if len(team.students.all()) < team.assignment.requirements.max_group_size:
                team.students.add(request.user.student)
                team.save()
            else:
                return HttpResponse("Cannot complete operation. This team is now full!")

            return HttpResponseRedirect(reverse('home'))
        else:
            logout(request)  # Clear store session
            return HttpResponse("Oops something went wrong!!")
    else:
        return HttpResponse("Not logged in!")


def student_home(request):
    if request.user.is_authenticated():
        context_dict = {}
        user = request.user

        context_dict['username'] = user.username
        context_dict['assignments'] = Assignment.objects.filter(students__user=user)
        context_dict['groups'] = Group.objects.filter(students__user=user)

        profile = request.user.student
        assignments = profile.assignment_set.all()

        context_dict['username'] = user.username
        context_dict['assignments'] = Assignment.objects.filter(students__user=user)
        context_dict['groups'] = Group.objects.filter(students__user=user)

        htmlStr = MyCalendar(firstweekday=calendar.SUNDAY, assignments=assignments).formatmonth(date.today().year,
                                                                                                date.today().month)
        context_dict['calendar'] = mark_safe(htmlStr)

        return render(request, 'student_home.html', context_dict)
    else:
        return HttpResponse("Not logged in!")


def instructor_home(request):
    if request.user.is_authenticated():

        context_dict = {}
        user = request.user

        profile = request.user.instructor
        courses = []
        deadlines = []
        assignments = profile.assignment_set.all()
        for a in assignments:
            if a.course not in courses:
                courses.append(a.course)

        context_dict['username'] = user.username
        context_dict['courses'] = courses
        context_dict['assignments'] = assignments

        htmlStr = MyCalendar(firstweekday=calendar.SUNDAY, assignments=assignments).formatmonth(date.today().year,
                                                                                                date.today().month)
        context_dict['calendar'] = mark_safe(htmlStr)

        return render(request, 'instructor_home.html', context_dict)
    else:
        return HttpResponse("Since you're logged in, you can see this text!")


def parse(rated_qualifs):
    lines = rated_qualifs.splitlines()

    list = []

    for line in lines:
        words = line.split()

        if len(words) == 2:
            try:
                qualif = str(words[0])
                rating = int(words[1])

                if 1 <= rating <= 4:
                    qualification = Qualification.objects.get_or_create(name=qualif)[0]
                    list.append(RatedQualification.objects.get_or_create(qualification=qualification, rating=rating)[0])
                else:
                    return -1
            except Exception, e:
                print e
                return -1
        else:
            return -1

    return list


@login_required
def assignment_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated():

            profile = request.user.instructor

            assign_form = AssignmentForm(data=request.POST)
            req_form = RequirementsForm(data=request.POST)
            rated_qualif_form = RatedQualificationForm(data=request.POST)
            datetime_form = DateTimeFieldForm(data=request.POST)

            # If the two forms are valid
            if assign_form.is_valid() and \
                    req_form.is_valid() and \
                    rated_qualif_form.is_valid() and \
                    datetime_form.is_valid():

                # Requirements
                min_group_size = req_form.cleaned_data['min_group_size']
                max_group_size = req_form.cleaned_data['max_group_size']
                requirements = Requirement.objects.create(min_group_size=min_group_size, max_group_size=max_group_size)
                requirements.save()
                rated_qualifs = rated_qualif_form.cleaned_data['rated_qualifications']
                rated_qualifs = parse(rated_qualifs)
                [requirements.rated_qualifications.add(rq) for rq in rated_qualifs]
                requirements.save()

                # Deadline
                datetime = datetime_form.cleaned_data['deadline']
                print datetime

                # Assignments
                assign = Assignment.objects.create(
                    name=assign_form.cleaned_data['name'],
                    instructor=profile,
                    course=assign_form.cleaned_data['course'],
                    deadline=datetime,
                    requirements=requirements,
                )
                assign.save()

                try:
                    file = request.FILES['students']
                    for line in file:
                        id = line.rstrip('\r').rstrip('\n')
                        s = Student.objects.get(matriculationNumber=id)
                        assign.students.add(s)
                    assign.save()
                except:
                    print "invalid student number found"

            else:
                print assign_form.errors
    else:
        assign_form = AssignmentForm()
        req_form = RequirementsForm()
        rated_qualif_form = RatedQualificationForm()
        datetime_form = DateTimeFieldForm()

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    # Adds our results list to the template context under name pages.
    context_dict['assign_form'] = assign_form
    context_dict['req_form'] = req_form
    context_dict['rated_qualif_form'] = rated_qualif_form
    context_dict['datetime_form'] = datetime_form

    # Render the template depending on the context.
    return render(request, 'assignment_create.html', context_dict)


@login_required
def assignment_view(request, assignment_id):
    # ------------------------------use populate.py script--------------------------
    if request.user.is_authenticated():

        # Construct a dictionary to pass to the template engine as its context.
        context_dict = {}
        user = request.user

        if hasattr(request.user, 'student'):
            profile = request.user.student
            user_type = "student"
        elif hasattr(request.user, 'instructor'):
            profile = request.user.instructor
            user_type = "instructor"
        else:
            logout(request)  # Clear store session
            return HttpResponse("Oops something went wrong!!")

        # Return a rendered response to send to the client.
        context_dict['user_type'] = user_type
        context_dict['username'] = user.username
        assignment = Assignment.objects.get(id=assignment_id)
        groups = assignment.group_set.all()

        context_dict['assignment'] = assignment
        context_dict['groups'] = groups
        context_dict['no_group'] = getNoGroup(assignment)
        return render(request, 'assignment_view.html', context_dict)
    else:
        return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def team_create(request, assignment_id):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    assignment = Assignment.objects.get(id=assignment_id)
    limit = assignment.requirements.max_group_size
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        qs = getNoGroupQS(assignment)
        group_form = GroupForm(data=request.POST, limit=limit, students_qs=qs)

        # If the two forms are valid...
        if group_form.is_valid():
            assignment = Assignment.objects.get(id=assignment_id)
            group = Group.objects.create(
                name=group_form.cleaned_data['name'],
                assignment=assignment,
            )

            group.students = group_form.cleaned_data['students']
            group.save()

            # Update our variable to tell the template registration was successful.
            registered = True
            return HttpResponseRedirect(reverse('assignment_view', args=[assignment_id]))

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print group_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        qs = getNoGroupQS(assignment)
        group_form = GroupForm(limit=limit, students_qs=qs)

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    context_dict['username'] = request.user.username
    # Adds our results list to the template context under name pages.
    context_dict['assignment_id'] = assignment_id
    context_dict['group_form'] = group_form
    context_dict['registered'] = registered

    # Render the template depending on the context.
    return render(request, 'team_create.html', context_dict)


@login_required
def notifications_view(request):
    # ------------------------------use populate.py script--------------------------
    if request.user.is_authenticated():

        # Construct a dictionary to pass to the template engine as its context.
        context_dict = {}
        user = request.user

        if hasattr(request.user, 'student'):
            student = request.user.student
            user_type = "student"
        else:
            logout(request)  # Clear store session
            return HttpResponse("Oops something went wrong!!")

        # Return a rendered response to send to the client.

        not_accepted = []
        groups = Group.objects.filter(students__in=[student])
        for group in groups:
            if hasattr(group, 'notification'):
                result = group.notification.accepted.filter(id=student.id)
                if not (student in result):
                    not_accepted.append(group)
            else:
                not_accepted.append(group)

        context_dict['not_accepted'] = not_accepted
        return render(request, 'notifications.html', context_dict)
    else:
        return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def notification_accept(request, group_id):
    # ------------------------------use populate.py script--------------------------
    if request.user.is_authenticated():

        # Construct a dictionary to pass to the template engine as its context.
        context_dict = {}
        user = request.user

        if hasattr(request.user, 'student'):
            student = request.user.student
            user_type = "student"
        else:
            logout(request)  # Clear store session
            return HttpResponse("Oops something went wrong!!")

        try:
            group = Group.objects.get(id=group_id)
            if not hasattr(group, 'notification'):
                notif = Notification.objects.create(
                    group=group,
                )
                notif.save()

            result = group.notification.accepted.filter(id=student.id)
            if not (student in result):
                group.notification.accepted.add(student)
                group.notification.save()

            return HttpResponse("Success")
        except:
            return HttpResponse("Fail")
    else:
        return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def notification_reject(request, group_id):
    # ------------------------------use populate.py script--------------------------
    if request.user.is_authenticated():

        # Construct a dictionary to pass to the template engine as its context.
        context_dict = {}
        user = request.user

        if hasattr(request.user, 'student'):
            student = request.user.student
            user_type = "student"
        else:
            logout(request)  # Clear store session
            return HttpResponse("Oops something went wrong!!")

        try:
            group = Group.objects.get(id=group_id)
            group.delete()
            return HttpResponse("Success")
        except:
            return HttpResponse("Fail")
    else:
        return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


def getNoGroupQS(assignment):
    queryset_all = Student.objects.all()
    included_pks = []
    for student in assignment.students.all():
        group = student.group_set.filter(assignment_id=assignment.id)
        if group.count() == 0:
            included_pks.append(student.pk)
    queryset = queryset_all.filter(pk__in=included_pks)
    return queryset


def getNoGroup(assignment):
    no_group = []
    for student in assignment.students.all():
        group = student.group_set.filter(assignment_id=assignment.id)
        if group.count() == 0:
            no_group.append(student)

    return no_group


def about_us(request):
    return render(request, 'about-us.html', {})


def uta_users(request):
    return render(request, 'uta_users.html', {})


def help(request):
    return render(request, 'help.html', {})


@login_required
def studentprofile(request):
    context_dict = {}
    if request.user.is_authenticated():

        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = StudentUpdateForm(request.POST, instance=request.user.student)
            ratedQualification_form = RatedQualificationForm(data=request.POST)
            print profile_form
            ratedQualification_form.is_valid()
            if user_form.is_valid() and profile_form.is_valid() :
                user_form.save()
                profile_form.save()

                rated_qualifs = ratedQualification_form.cleaned_data['rated_qualifications']
                rated_qualifs = parse(rated_qualifs)
                [request.user.student.rated_qualifications.add(rq) for rq in rated_qualifs]
                request.user.student.save()
                print 'saved'
            else:
                return HttpResponse("Oops something went wrong!!")

            return render(request, 'student_profile.html', context_dict)
        else:
            user_form = UserUpdateForm(instance=request.user)
            context_dict['user_form'] = user_form
            profile_form = StudentUpdateForm(instance=request.user.student)
            context_dict['profile_form'] = profile_form
            ratedQualification_form =  RatedQualificationForm()
            context_dict['rated_qualif_form'] = ratedQualification_form

            return render(request, 'student_profile.html', context_dict)

    else:
        logout(request)  # Clear store session
        return HttpResponse("Oops something went wrong!!")

@login_required
def instructorprofile(request):
    context_dict = {}
    if request.user.is_authenticated():

        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = InstructorUpdateForm(request.POST, instance=request.user.instructor)
            print profile_form
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                print 'saved'
            else:
                return HttpResponse("Oops something went wrong!!")

            return HttpResponseRedirect(reverse('instructorprofile'))
        else:
            user_form = UserUpdateForm(instance=request.user)
            context_dict['user_form'] = user_form
            profile_form = InstructorUpdateForm(instance=request.user.instructor)
            context_dict['profile_form'] = profile_form

            return render(request, 'instructor_profile.html', context_dict)

    else:
        logout(request)  # Clear store session
        return HttpResponse("Oops something went wrong!!")

