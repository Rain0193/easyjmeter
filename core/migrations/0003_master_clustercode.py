# Generated by Django 2.1.5 on 2019-04-02 08:57

import core.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190129_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='clusterCode',
            field=models.CharField(max_length=64, null=True, validators=[core.validator.validate_empty_str]),
        ),
    ]
