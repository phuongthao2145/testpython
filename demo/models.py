from django.db import models

# Create your models here.
from django.db import models
class Demo(models.Model):
    patientcode = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, null=True)
    f0 = models.ForeignKey('Demo', on_delete=models.RESTRICT, null=True, related_name='f0fk', blank=True)
    f1 = models.ForeignKey('Demo', on_delete=models.RESTRICT, null=True, related_name='f1fk', blank=True)
    f2 = models.ForeignKey('Demo', on_delete=models.RESTRICT, null=True, related_name='f2fk', blank=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.patientcode
