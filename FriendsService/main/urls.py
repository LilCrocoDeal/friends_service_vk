from django.urls import path, re_path

from . import views


urlpatterns = [
    path('account/registration/', views.RegistrationView.as_view(), name='registration'),
    path('account/login/', views.LoginView.as_view(), name='login'),
    path('account/logout/', views.LogoutView.as_view(), name='logout'),
    path('friends/', views.FriendsView.as_view(), name='friends'),
    path('friends/delete/', views.FriendsDeleteView.as_view(), name='friends_delete'),
    path('requests/send/', views.RequestsSendView.as_view(), name='requests_send'),
    path('requests/', views.RequestsView.as_view(), name='requests'),
    path('requests/manage/', views.RequestsManageView.as_view(), name='requests_manage'),
    path('requests/delete/', views.RequestsDeleteView.as_view(), name='requests_delete'),
    re_path(r'info$', views.InfoView.as_view(), name='info'),
]