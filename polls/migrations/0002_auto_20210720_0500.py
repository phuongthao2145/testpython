# Generated by Django 3.1.4 on 2021-07-20 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateField(verbose_name='date published'),
        ),
    ]
