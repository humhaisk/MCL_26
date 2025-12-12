from django.contrib import admin
from core import models
from django.contrib.auth.models import User
#MCL26 pas 123456789
# Register your models here.
admin.site.register(models.TeamDetails)
admin.site.register(models.PlayerDetails)
# admin.site.register(User)
