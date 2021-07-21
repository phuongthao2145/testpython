# Generated by Django 3.1.4 on 2021-07-21 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0006_auto_20210720_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='demo',
            name='isolation_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='demo.province'),
        ),
        migrations.AddField(
            model_name='district',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='demo.city'),
        ),
        migrations.AddField(
            model_name='province',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='demo.district'),
        ),
        migrations.AlterField(
            model_name='demo',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='province', to='demo.province'),
        ),
    ]
