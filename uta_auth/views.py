from django.http import *
from django.contrib.auth import *
from uta_auth.forms import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from uta_models.models import Student



def register(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        user_type = request.POST.get('user_type')

        return HttpResponseRedirect(reverse('register_user', args=[user_type]))
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'uta_auth/register.html', {})


def register_user(request, user_type):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        if user_type == "student":
            profile_form = StudentForm(data=request.POST)
        else:
            profile_form = InstructorForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            # if 'picture' in request.FILES:
            #   profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        if user_type == "student":
            profile_form = StudentForm()
        else:
            profile_form = InstructorForm()

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    # Adds our results list to the template context under name pages.
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['user_type'] = user_type
    context_dict['registered'] = registered

    # Render the template depending on the context.
    return render(request, 'uta_auth/register_user.html', context_dict)


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))
