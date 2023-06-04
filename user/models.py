from enum import unique
from django.db import models
from chor.models import User
# from chor.models import Chor

# class ChorUser(models.Model):
#     inneruser = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE
#     )
#     email = models.OneToOneField(
#         inneruser.email,
#         on_delete=models.CASCADE
#     )


class UserRoleName(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    @classmethod
    def get_default_pk(cls):
        userolename, created = cls.objects.get_or_create(name='member')
        return userolename.pk

    def __str__(self) -> str:
        return self.name


class UserChorRole(models.Model):
    chor = models.ForeignKey(
        "chor.Chor", #declared in Chor.models
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        UserRoleName,
        on_delete=models.SET_DEFAULT,
        default=UserRoleName.get_default_pk
    )
    description = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['chor', 'user']]

    def __str__(self) -> str:
        return ' - '.join((str(self.chor), str(self.user), str(self.role)))
