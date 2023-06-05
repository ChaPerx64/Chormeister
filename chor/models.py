from django.db import models
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from user.models import UserChorRole, ChorRole


class Chor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    owner = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name='chor_owned'
    )
    created_by = models.CharField(
        max_length=320,
        editable=False,
    )
    participants = models.ManyToManyField(
        User,
        through=UserChorRole,
        editable=False,
    )

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.created_by:
            if self.owner:
                self.created_by = f'user.id: {self.owner.pk}, username: {self.owner.username}'
            else:
                raise FieldError(
                    'chor.owner field cannot be NULL during creation')
        super(Chor, self).save(*args, **kwargs)

    def make_admin(self, user: User):
        userchorrole, created = UserChorRole.objects.get_or_create(
            user=user,
            chor=self,
        )
        userchorrole.role = ChorRole.get_admin_role()
        userchorrole.save()

    def make_member(self, user: User):
        userchorrole, created = UserChorRole.objects.get_or_create(
            user=user,
            chor=self,
        )
        userchorrole.role = ChorRole.get_member_role()
        userchorrole.save()

    def kick_member(self, user: User):
        userchorrole = get_object_or_404(UserChorRole, chor=self, user=user)
        userchorrole.delete()
    
    def user_is_admin(self, user: User):
        try:
            if user.userchorrole_set.get(chor=self).role == ChorRole.get_admin_role():
                return True
            return False
        except ObjectDoesNotExist:
            return False
    
    def user_is_member(self, user: User):
        try:
            if user.userchorrole_set.get(chor=self).role == ChorRole.get_member_role():
                return True
            return False
        except:
            return False
    
    def user_is_owner(self, user: User):
        if self.owner:
            if user.id == self.owner.id:
                return True
        return False



class Song(models.Model):
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
