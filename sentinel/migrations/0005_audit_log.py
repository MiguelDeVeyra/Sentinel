# Generated by Django 2.2.7 on 2019-12-08 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentinel', '0004_auto_20191209_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='audit_log',
            fields=[
                ('auditID', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('notifID', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('userAction', models.CharField(max_length=100)),
            ],
        ),
    ]
