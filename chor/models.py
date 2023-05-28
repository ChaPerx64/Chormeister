from django.db import models

# Create your models here.

class Chor (models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Song (models.Model):
    chor = models.ForeignKey(
        Chor,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

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