from django.contrib import admin
from .models import Student,StudentDocument,StudentApplicationStatus,StudentCredentials,StudentPayment
# Register your models here.

admin.site.register(Student)
admin.site.register(StudentDocument)
admin.site.register(StudentApplicationStatus)
admin.site.register(StudentCredentials)
admin.site.register(StudentPayment)