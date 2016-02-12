from django.http import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponseRedirect(reverse('login'))


def home(request):

    #if not request.user.is_authenticated():
    # return HttpResponse("You are logged in.")

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'index.html', context_dict)

    #else:
    # return HttpResponse("You are not logged in.")
