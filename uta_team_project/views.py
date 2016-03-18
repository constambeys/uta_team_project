from django.http import *
from django.contrib.auth import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from uta_models.models import *
from forms import *
from uta_models.models import Student
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar
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
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'index.html', {})


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

    context_dict = {}
    # The assignment that the user has selected
    assignment = Assignment.objects.get(id=assignment_id)
    requirements = assignment.requirements
    groups = Group.objects.filter(assignment__name=assignment.name)

    groups_benefits = Matching(groups, requirements, request.user.student).rank()

    ranked_groups = [g for (g, b) in groups_benefits]

    print ranked_groups

    context_dict['ranked_groups'] = ranked_groups
    if ranked_groups > 0:
        context_dict['top_group'] = ranked_groups[0]
    context_dict['assignment'] = assignment
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
        deadlines = []
        for a in profile.assignment_set.all():
            deadlines.append(a.deadline.date())

        context_dict['username'] = user.username
        context_dict['assignments'] = Assignment.objects.filter(students__user=user)
        context_dict['groups'] = Group.objects.filter(students__user=user)

        htmlStr = MyCalendar(firstweekday=calendar.SUNDAY, deadlines=deadlines).formatmonth(date.today().year,
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
        for a in profile.assignment_set.all():
            deadlines.append(a.deadline.date())
            if a.course not in courses:
                courses.append(a.course)

        context_dict['username'] = user.username
        context_dict['courses'] = courses
        context_dict['assignments'] = profile.assignment_set.all()

        htmlStr = MyCalendar(firstweekday=calendar.SUNDAY, deadlines=deadlines).formatmonth(date.today().year,
                                                                                            date.today().month)
        context_dict['calendar'] = mark_safe(htmlStr)

        return render(request, 'instructor_home.html', context_dict)
    else:
        return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def assignment_create(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        assign_form = AssignmentForm(data=request.POST)

        # If the two forms are valid...
        if assign_form.is_valid():
            # Save the user's form data to the database.
            assign = assign_form.save()

            try:
                file = request.FILES['students']
                for line in file:
                    id = line.rstrip('\r').rstrip('\n')
                    s = Student.objects.get(matriculationNumber=id)
                    assign.students.add(s)
                assign.save()
            except:
                print "invalid student number found"

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print assign_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        assign_form = AssignmentForm()

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    # Adds our results list to the template context under name pages.
    context_dict['assign_form'] = assign_form
    context_dict['registered'] = registered

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
        elif hasattr(request.user, 'instructor'):
            profile = request.user.instructor
        else:
            logout(request)  # Clear store session
            return HttpResponse("Oops something went wrong!!")

        # Return a rendered response to send to the client.
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

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        group_form = GroupForm(data=request.POST)

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

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print group_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        group_form = GroupForm()

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
def requirements_create(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        req_form = RequirementsForm(data=request.POST)

        # If the two forms are valid...
        if req_form.is_valid():
            # Save the user's form data to the database.
            assign = req_form.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print req_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        req_form = RequirementsForm()

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    # Adds our results list to the template context under name pages.
    context_dict['req_form'] = req_form
    context_dict['registered'] = registered

    # Render the template depending on the context.
    return render(request, 'requirements_create.html', context_dict)


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


def getNoGroup(assignment):
    no_group = []
    for student in assignment.students.all():
        group = student.group_set.filter(assignment_id=assignment.id)
        if group.count() == 0:
            no_group.append(student)

    return no_group
