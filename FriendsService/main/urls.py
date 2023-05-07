from django.urls import path, re_path

from . import views


urlpatterns = [
    path('friends/', views.FriendsView.as_view()),
    path('friends/delete/', views.FriendsDeleteView.as_view()),
    path('requests/send/', views.RequestsSendView.as_view()),
    path('requests/', views.RequestsView.as_view()),
    path('requests/manage/', views.RequestsManageView.as_view()),
    re_path(r'info$', views.InfoView.as_view()),
]