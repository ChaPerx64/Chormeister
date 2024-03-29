# Generated by Django 4.2.5 on 2023-09-17 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChorRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='InviteLink',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('chor', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='chor.chor')),
            ],
        ),
        migrations.CreateModel(
            name='UserChorRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('chor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chor.chor')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.chorrole')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('chor', 'user')},
            },
        ),
    ]
