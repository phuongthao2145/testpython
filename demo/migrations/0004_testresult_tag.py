# Generated by Django 3.1.4 on 2021-07-20 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0003_auto_20210720_0515'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='tag',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]