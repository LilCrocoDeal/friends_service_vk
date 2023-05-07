from django.urls import path

from . import views


urlpatterns = [
    path('friends/', views.FriendsView.as_view()),
    path('requests/', views.RequestsView.as_view()),
]