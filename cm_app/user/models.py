from django.db import models
from django.contrib.auth.models import User
# from chor.models import User
from uuid import uuid4

class ChorRole(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    @classmethod
    def get_member_role(cls):
        memberrole, created = cls.objects.get_or_create(name='member')
        return memberrole

    @classmethod
    def get_admin_role(cls):
        adminrole, created = cls.objects.get_or_create(name='admin')
        return adminrole

    def __str__(self) -> str:
        return self.name


class UserChorRole(models.Model):
    chor = models.ForeignKey(
        "chor.Chor",  # declared in Chor.models
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        ChorRole,
        on_delete=models.SET_DEFAULT,
        default=ChorRole.get_member_role().pk
    )
    description = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['chor', 'user']]

    def __str__(self) -> str:
        return ' - '.join((str(self.chor), str(self.user), str(self.role)))


class InviteLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    chor = models.OneToOneField(
        "chor.Chor",     # declared in Chor.models
        on_delete=models.CASCADE,
        editable=False
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    # def as_url_param(self):
    #     return f''
