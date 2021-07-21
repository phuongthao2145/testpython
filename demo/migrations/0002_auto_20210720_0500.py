# Generated by Django 3.1.4 on 2021-07-20 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cityname', models.CharField(max_length=200)),
                ('quarantined', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disname', models.CharField(max_length=200)),
                ('quarantined', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='demo',
            name='test_result',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='province',
            name='quarantined',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='demo',
            name='created_at',
            field=models.DateTimeField(verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='demo',
            name='expiration',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date expire'),
        ),
        migrations.AddField(
            model_name='demo',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='demo.city'),
        ),
        migrations.AddField(
            model_name='demo',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='demo.district'),
        ),
    ]