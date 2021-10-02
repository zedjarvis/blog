from django.shortcuts import redirect, render
from django.contrib import messages
# Create your views here.

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


# custom user creation template in forms.py
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from .models import Notifications


#######################################################
# Admin Dashboard
#######################################################
@staff_member_required(login_url="login")
def dashBoard(request):

    # none staff members not allowed in this page
    if not request.user.is_staff:
        return redirect('profile')

        # demo dashboard page
    context = {}

    return render(request,
                  'accounts/dashboard.html', context)


##########################################################
# User Profile Page
##########################################################
@login_required
def userProfile(request):
    notifications = Notifications.objects.filter(user=request.user,
                                                 viewed=False)
    n = len(notifications)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Account Update Succesful")
            return redirect('profile')

    else:
        # passing the instances to prefill form with db data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'notifications': notifications,
        'n': n
    }

    return render(request,
                  'accounts/profile.html', context)


###############################################################
# Change Password Page
###############################################################
@login_required
def changePassword(request):

    notifications = Notifications.objects.filter(user=request.user,
                                                 viewed=False)
    n = len(notifications)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,
                             'success')

            return redirect('changepassword')
        else:
            messages.error(request,
                           'error')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form,
        'n': n,
        'notifications': notifications
    })


################################################################
# Error Page for logged in users
################################################################
@login_required
def dashBoardErrorPage(request):
    # error page for logged in users

    notifications = Notifications.objects.filter(user=request.user,
                                                 viewed=False)
    n = len(notifications)

    context = {'n': n,
               'notifications': notifications}
    return render(request,
                  'accounts/404.html', context)


#################################################################
# Notifications Page
#################################################################
@login_required
def notificationPage(request):

    notifications = Notifications.objects.filter(user=request.user)
    not_read = len([n for n in notifications if not n.viewed])
    for notification in notifications:
        if not notification.viewed:
            notification.viewed = True
            notification.save()

    context = {'notifications': notifications,
               'n': not_read
               }

    return render(request,
                  'accounts/notifications.html', context)


#################################################################
# Site admins Task Page
#################################################################
@staff_member_required
def taskBoard(request):

    # none staff members not allowed in this page
    if not request.user.is_staff:
        return redirect('profile')

        # demo dashboard page
    context = {}

    return render(request,
                  'accounts/taskboard.html', context)


#################################################################
# User Registration Page
#################################################################
def registerUser(request):

    # authenticated users are not allowed on this page
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        # user registration page
        form = CreateUserForm()  # custom userform

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request,
                                 user.upper() + ', account created!')
                # send new user to login page
                # TO DO: send a verificatio email
                return redirect('login')

    context = {'form': form}

    return render(request,
                  'accounts/registration/register.html', context)


####################################################################
# User Login Page
####################################################################
def loginUser(request):

    # authenticated users are not allowed on this page
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            # get user email and password
            username = request.POST.get("username")
            password = request.POST.get("password")

            # authenticate the email and password
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.info(request,
                              'Username or password is incorrect!')

    return render(request,
                  'accounts/registration/login.html')


####################################################################
# User Logout URL
####################################################################
def logoutUser(request):
    # logout the user
    logout(request)
    return redirect('login')


#####################################################################
# Password Reset Page
#####################################################################
def resetPassword(request):
    # forgot password page

    # authenticated users are not allowed on this page
    if request.user.is_authenticated:
        return redirect('profile')
    context = {}

    return render(request,
                  'accounts/registration/forgot-password.html', context)


######################################################################
# General Error Page
######################################################################
def generalErrorPage(request):
    return render(request,
                  'accounts/error-404.html')
