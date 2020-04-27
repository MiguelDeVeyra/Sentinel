# Generated by Django 2.2 on 2020-02-04 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sentinel', '0016_auto_20200204_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audit_log',
            name='email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sentinel.end_user'),
        ),
    ]