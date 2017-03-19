from django.contrib import admin

# Register your models here.
from weibo_app1 import models

admin.site.register(models.person)
admin.site.register(models.massage)
admin.site.register(models.status)