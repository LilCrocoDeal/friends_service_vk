from django.db import models


class Friends(models.Model):
    first_user = models.ForeignKey('auth.User', related_name="request", on_delete=models.CASCADE)
    second_user = models.ForeignKey('auth.User', related_name="accepted", on_delete=models.CASCADE)


class FriendshipRequests(models.Model):
    to_user = models.ForeignKey('auth.User', related_name="acceptor", on_delete=models.CASCADE)
    from_user = models.ForeignKey('auth.User', related_name="inviter", on_delete=models.CASCADE)
    status = models.BooleanField()
