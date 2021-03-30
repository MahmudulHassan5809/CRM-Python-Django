from django.contrib import admin
from .models import Lead,Event,TaskAssign

# Register your models here.
admin.site.register(Lead)
admin.site.register(Event)
admin.site.register(TaskAssign)
