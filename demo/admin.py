from django.contrib import admin

# Register your models here.
from .models import *
class DemoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info', {'fields': ('patientcode', 'name', 'status', 'phone', 'address', 'province', 'district', 'city', 'created_at')}),
        (None, {'fields': ('f_status', 'test_result', 'expiration','isolation_area')})
    ]
    list_display = ('id', 'patientcode', 'name', 'status', 'f_status', 'phone',
                    'address', 'province', 'district', 'city', 'created_at', 'expiration', 'test_result','isolation_area')
    search_fields = ['patientcode']

class ProvinceAdmin(admin.ModelAdmin):
    fields = ['proname', 'slug', 'district']
    list_display = ('id', 'proname', 'slug', 'district')

class DistrictAdmin(admin.ModelAdmin):
    fields = ['disname', 'slug', 'city']
    list_display = ('id', 'disname', 'slug', 'city')


class CityAdmin(admin.ModelAdmin):
    fields = ['cityname', 'slug']
    list_display = ('id', 'cityname', 'slug')

class TestResultAdmin(admin.ModelAdmin):
    fields = ['testname', 'tag', 'slug']
    list_display = ('id', 'testname', 'tag', 'slug')

class StatusAdmin(admin.ModelAdmin):
    fields = ['sname', 'tag']
    list_display = ('id', 'sname', 'tag')


admin.site.register(Demo, DemoAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(TestResult, TestResultAdmin)
admin.site.register(Status, StatusAdmin)
