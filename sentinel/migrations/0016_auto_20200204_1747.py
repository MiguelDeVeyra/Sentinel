# Generated by Django 2.2 on 2020-02-04 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentinel', '0015_auto_20200204_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audit_log',
            name='notifID',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
