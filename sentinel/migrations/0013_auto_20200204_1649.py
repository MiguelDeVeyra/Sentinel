# Generated by Django 2.2 on 2020-02-04 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sentinel', '0012_auto_20200204_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity_log',
            name='email',
            field=models.ForeignKey(default='intruder', on_delete=django.db.models.deletion.PROTECT, to='sentinel.end_user'),
        ),
    ]
