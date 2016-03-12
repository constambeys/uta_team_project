from django.http import *
from django.contrib.auth import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from uta_models.models import *
from forms import *


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
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'index.html', {})


@login_required
def home(request):
    if request.user.is_authenticated():

        # Construct a dictionary to pass to the template engine as its context.
        context_dict = {}
        user = request.user
        context_dict['user'] = user
        if hasattr(request.user, 'student'):
            profile = request.user.student
            context_dict['student'] = profile
            context_dict['groups'] = profile.group_set.all()
        elif hasattr(request.user, 'instructor'):
            profile = request.user.instructor
            context_dict['instructor'] = profile
        else:
            logout(request)  # Clear store session
            return HttpResponse("Oops something went wrong!!")  # Return a rendered response to send to the client.

        context_dict['assignments'] = profile.assignment_set.all()
        return render(request, 'student_home.html', context_dict)
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

        context_dict['groups'] = groups
        context_dict['no_group'] = getNoGroup(assignment)
        return render(request, 'assignment_view.html', context_dict)
    else:
        return HttpResponse("Since you're logged in, you can see this text!")


def group_create(request):
    if request.user.is_authenticated():
        pass
        # Working
    else:
        return HttpResponse("Since you're logged in, you can see this text!")


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
