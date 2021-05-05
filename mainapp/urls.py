from django.urls import path
from . import views


urlpatterns = [
    path('', views.mainView, name='mainView'),
    path('register/', views.registrationView, name='registrationView'),
    path('add_friends/', views.addFriendsView, name='addFriendsView'),
    path('my_friends/', views.myFriendsView, name='myFriendsView'),
    path('friends_requests/', views.friendsRequestsView, name='friendsRequestsView'),
    path('enter_secret_code/', views.enterSecretCodeView, name='enterSecretCodeView'),
]