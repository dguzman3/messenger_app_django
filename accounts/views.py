from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import CustomUserCreationForm
from .models import CustomUser, FriendRequest

class HomepageView(TemplateView):
    template_name = 'homepage.html'

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1']
            )
            login(request, new_user)
            return HttpResponseRedirect('/')
        else:
            print(request.POST, form.errors)
            return render(request, 'auth/signup.html', 
                {'form': form, 'error': form.errors})
    else:
        form = CustomUserCreationForm()
        return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'username or password not correct')
            return HttpResponseRedirect('/login/')    
    else:    
        return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def send_friend_request(request, userID):
    from_user = request.user
    to_user = CustomUser.objects.get(id=userID)
    friend_request, created = FriendRequest.objects.get_or_create(
        from_user=from_user, 
        to_user=to_user
    )
    if created:
        messages.error(request, 'friend request sent')
        return HttpResponseRedirect('/friends/')
    else:
        messages.error(request, 'friend request was already sent')
        return HttpResponseRedirect('/friends/')

@login_required
def accept_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()

        messages.error(request, 'friend request accepted')
        return HttpResponseRedirect('/friends/')
    else:
        messages.error(request, 'friend request not accepted')
        return HttpResponseRedirect('/friends/')


@login_required
def friend_list(request):
    context = {}
    context["users"] = CustomUser.objects.exclude(
            is_staff=True
        ).exclude(
            username=request.user.username
        ).exclude(
            friends__id=request.user.id
        )
    context["friend_requests"] = FriendRequest.objects.filter(
            to_user=request.user.id
        )
    context["friends"] = CustomUser.objects.filter(
            friends__id=request.user.id
        )
    return render(request, "social/friend_list.html", context)

@login_required
def remove_friend(request, userID):
    current_user = CustomUser.objects.get(id=request.user.id)
    friend = CustomUser.objects.get(id=userID)

    current_user.friends.remove(friend)
    friend.friends.remove(current_user)

    return HttpResponseRedirect('/friends/')