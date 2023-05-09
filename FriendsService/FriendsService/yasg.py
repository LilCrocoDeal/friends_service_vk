from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Friends Service",
      default_version='1.0.0',
      description="This site allows users to find friends.\n\n\n"
                  "How to use:\n\n"
                  "- To create your profile use /account/registration/ and write down your username and password. "
                  "Username must be unique.\n\n"
                  "- To authorize use /account/login/ and enter your login with password. If they "
                  "are correct, response will give you token you have to copy and paste in field "
                  "\"Authorize\" upper in format: \"Token {token_from_response}\".\n\n"
                  "- You can add friend by sending request to existing user in /requests/send/.\n\n"
                  "- Check all friend requests related with you in /requests/.\n\n"
                  "- Accept or reject friend requests from user in /requests/manage/.\n\n"
                  "- View info about your interactions on this site with any user in /info.\n\n"
                  "- Check all your friends in /friends/.\n\n"
                  "- Delete your friend in /friends/delete/. \n\n"
                  "- To logout please visit /account/logout/. Also please logout in \"Authorize\" upper.\n\n",
      terms_of_service="https://www.google.com/policies/terms/",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]