from django.db import models

# Create your models here.
class Demo(models.Model):
    patientcode = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    status = models.ForeignKey('Status', on_delete=models.RESTRICT, null=True, blank=True)
    f_status = models.ForeignKey('Demo', on_delete=models.RESTRICT, null=True, related_name='f0fk', blank=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100, null=True)
    province = models.ForeignKey('Province', on_delete=models.RESTRICT, null=True, blank=True,related_name='province')
    district = models.ForeignKey('District', on_delete=models.RESTRICT, null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField('date published')
    updated_at = models.DateTimeField(auto_now=True, blank=True,  null=True,)
    expiration = models.DateTimeField('date expire', blank=True,  null=True)
    test_result = models.ForeignKey('TestResult', on_delete=models.RESTRICT, null=True, blank=True)
    isolation_area = models.ForeignKey('Province', on_delete=models.RESTRICT, null=True, blank=True)
    def __str__(self):
        return self.patientcode
class Province(models.Model):
    proname = models.CharField(max_length=200)
    quarantined = models.IntegerField(null=True, blank=True)
    slug = models.CharField(max_length=200, null=True)
    district = models.ForeignKey('District', on_delete=models.RESTRICT, null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.proname

class District(models.Model):
    disname = models.CharField(max_length=200)
    quarantined = models.IntegerField(null=True, blank=True)
    slug = models.CharField(max_length=200, null=True)
    city = models.ForeignKey('City', on_delete=models.RESTRICT, null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.disname

class City(models.Model):
    cityname = models.CharField(max_length=200)
    quarantined = models.IntegerField(null=True, blank=True)
    slug = models.CharField(max_length=200, null=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.cityname

class TestResult(models.Model):
    testname = models.CharField(max_length=200)
    tag = models.CharField(max_length=100,null=True, blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.testname

class Status(models.Model):
    sname = models.CharField(max_length=200)
    tag = models.CharField(max_length=100, null=True, blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.sname