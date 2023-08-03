from django.contrib import admin

# Register your models here.
from .models import ChorRole, UserChorRole

admin.site.register(ChorRole)
admin.site.register(UserChorRole)