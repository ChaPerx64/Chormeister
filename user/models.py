from django.db import models
from chor.models import User


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
        "chor.Chor", #declared in Chor.models
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
