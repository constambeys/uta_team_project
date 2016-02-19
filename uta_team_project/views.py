from django.http import *
from django.contrib.auth import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from  uta_models.models import *


def index(request):
    return HttpResponseRedirect(reverse('login'))


@login_required
def home(request):
    if request.user.is_authenticated():

        # Construct a dictionary to pass to the template engine as its context.
        context_dict = {}
        user = request.user
        if hasattr(request.user, 'student'):
            profile = request.user.student
            context_dict['boldmessage'] = "Hello  " + user.first_name + " " + user.last_name + " " + profile.name
        elif hasattr(request.user, 'instructor'):
            profile = request.user.instructor
            context_dict['boldmessage'] = "Hello  " + user.first_name + " " + user.last_name + " " + profile.department
        else:
            logout(request)  # Clear store session
            return HttpResponse("Oops something went wrong!!")  # Return a rendered response to send to the client.

        return render(request, 'index.html', context_dict)
    else:
        return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def assignments_view(request):
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
        context_dict['assignments'] = profile.assignment_set.all()
        return render(request, 'assignments_view.html', context_dict)
    else:
        return HttpResponse("Since you're logged in, you can see this text!")


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
        groups  = assignment.group_set.all()

        context_dict['groups'] = groups
        context_dict['no_group'] = getNoGroup(assignment)
        return render(request, 'assignment_view.html', context_dict)
    else:
        return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

def getNoGroup(assignment):

    no_group = []
    for student in assignment.students.all():
        group = student.group_set.filter(assignment_id=assignment.id)
        if group.count()==0:
            no_group.append(student)

    return no_group