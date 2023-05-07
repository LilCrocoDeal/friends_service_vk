from django.db import models


class Friends(models.Model):
    core_person = models.CharField(max_length=50)
    friend = models.CharField(max_length=50)


class FriendshipRequests(models.Model):
    to_user = models.CharField(max_length=50)
    from_user = models.CharField(max_length=50)
    status = models.CharField(default="has been sent", max_length=21)
