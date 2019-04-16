# Generated by Django 2.1.5 on 2019-04-08 03:33

import core.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190407_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='resultMsg',
            field=models.TextField(null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AddField(
            model_name='slave',
            name='resultMsg',
            field=models.TextField(null=True, validators=[core.validator.validate_empty_str]),
        ),
    ]
