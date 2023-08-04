# Generated by Django 4.2.3 on 2023-07-06 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(null=True)),
                ('created_by', models.CharField(editable=False, max_length=320)),
                ('owner', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chor_owned', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('chor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chor.chor')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SongPropertyName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('chor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chor.chor')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SongPropertyValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chor.song')),
                ('songpropertyname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chor.songpropertyname')),
            ],
        ),
        migrations.CreateModel(
            name='SongPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dtofperformance', models.DateTimeField()),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chor.song')),
            ],
            options={
                'ordering': ['-dtofperformance'],
            },
        ),
    ]