from django.contrib import admin
from app01 import models
# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.ClassList)
admin.site.register(models.Campuses)
admin.site.register(models.Enrollment)