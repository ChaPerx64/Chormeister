from django.contrib import admin

# Register your models here.
from .models import UserRoleName, UserChorRole

admin.site.register(UserRoleName)
admin.site.register(UserChorRole)