from django.contrib.auth import logout
from django.urls import path
from .views import *


urlpatterns = [
    path('', HomepageView.as_view(), name="home"),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('send_friend_request/<int:userID>/', 
        send_friend_request, name="send_friend_request"),
    path('accept_friend_request/<int:requestID>/',
        accept_friend_request, name="accept_friend_request"),
    path('friends/', friend_list, name="friend_list"),
    path('remove_friend/<int:userID>/', remove_friend, 
        name="remove_friend"),
]