from django.http import *
from django.contrib.auth import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponseRedirect(reverse('login'))

@login_required
def home(request):
    if request.user.is_authenticated():
        # Construct a dictionary to pass to the template engine as its context.
        # Note the key boldmessage is the same as {{ boldmessage }} in the template!
        user = request.user
        if hasattr(request.user, 'userprofile'):
            profile = request.user.userprofile
        else:
            logout(request) #Clear store session
            return HttpResponse("Oops something went wrong!!")

        context_dict = {'boldmessage': "Hello  " + user.first_name + " " + user.last_name  + " " + profile.name}

        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.

        return render(request, 'index.html', context_dict)
    else:
        return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
