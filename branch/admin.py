from django.contrib import admin
from .models import Branch
# Register your models here.
class BranchAdmin(admin.ModelAdmin):

    list_display = ('__str__',)
    search_fields = ('branch_name',)
    list_per_page = 20


admin.site.register(Branch, BranchAdmin)
