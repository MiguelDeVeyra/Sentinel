# Generated by Django 2.2 on 2020-02-04 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sentinel', '0011_auto_20200204_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity_log',
            name='email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sentinel.end_user'),
        ),
    ]
