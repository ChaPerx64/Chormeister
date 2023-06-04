from django.db import models
from django.contrib.auth.models import User
from user.models import UserChorRole, UserRoleName

# Create your models here.

# DEFAULT ROLENAMES:
DEF_MEMBER_ROLENAME = 'member'
DEF_ADMIN_ROLENAME = 'admin'


class Chor (models.Model):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    owner = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        editable=False
    )
    created_by = models.CharField(
        max_length=255,
        editable=False,
    )

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.created_by:
            self.created_by = str(self.owner)
        super(Chor, self).save(*args, **kwargs)

    def make_admin(self, user: User):
        userchorrole, created = UserChorRole.objects.get_or_create(
            user=user,
            chor=self,
            role=UserRoleName.objects.get(name=DEF_ADMIN_ROLENAME),
        )
        userchorrole.save()

    def make_member(self, user: User):
        userchorrole, created = UserChorRole.objects.get_or_create(
            user=user,
            chor=self,
            role=UserRoleName.objects.get(name=DEF_MEMBER_ROLENAME),
        )
        userchorrole.save()


class Song (models.Model):
    chor = models.ForeignKey(
        Chor,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name',]

    def __str__(self) -> str:
        return ' - '.join((self.name, str(self.chor)))


class SongPropertyName (models.Model):
    chor = models.ForeignKey(
        Chor,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class SongPropertyValue (models.Model):
    songpropertyname = models.ForeignKey(
        SongPropertyName,
        on_delete=models.CASCADE
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return ' - '.join((str(self.song), str(self.songpropertyname), self.value))


class SongPerformance (models.Model):
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE
    )
    dtofperformance = models.DateTimeField()

    class Meta:
        ordering = ['-dtofperformance']

    def __str__(self) -> str:
        return ' - '.join((str(self.dtofperformance), str(self.song)))
