# Generated by Django 2.1.5 on 2019-04-08 06:23

import core.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190408_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='jmeterPath',
            field=models.CharField(max_length=100, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AddField(
            model_name='slave',
            name='jmeterPath',
            field=models.CharField(max_length=100, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='slave',
            name='resultMsg',
            field=models.TextField(null=True),
        ),
    ]
