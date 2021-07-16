from django.contrib import admin

# Register your models here.
from .models import Demo
class DemoAdmin(admin.ModelAdmin):
    #add column name to show for edit
    #fields = []
    #
    fieldsets = [
        ('Info', {'fields': ('patientcode', 'name', 'status', 'phone', 'address')}),
        (None, {'fields': ('f0', 'f1', 'f2')})
    ]
    list_display = ('id', 'patientcode', 'name', 'status', 'f0', 'f1', 'f2', 'phone', 'address')
    search_fields = ['patientcode']
admin.site.register(Demo, DemoAdmin)