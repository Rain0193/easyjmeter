# Generated by Django 2.1.5 on 2019-01-29 13:30

import core.validator
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateInstaceParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('templateInstaceCode', models.CharField(max_length=64, null=True)),
                ('name', models.CharField(max_length=32, null=True)),
                ('value', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='master',
            name='password',
            field=models.CharField(max_length=16, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AddField(
            model_name='master',
            name='userName',
            field=models.CharField(max_length=16, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AddField(
            model_name='task',
            name='modifyTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='clusterName',
            field=models.CharField(max_length=32, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='code',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='master',
            name='ip',
            field=models.GenericIPAddressField(null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='master',
            name='masterName',
            field=models.CharField(max_length=16, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='master',
            name='status',
            field=models.CharField(default='stop', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='slave',
            name='clusterCode',
            field=models.CharField(max_length=64, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='slave',
            name='ip',
            field=models.GenericIPAddressField(null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='task',
            name='taskName',
            field=models.CharField(max_length=16, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='task',
            name='userCode',
            field=models.CharField(max_length=64, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='taskruntime',
            name='masterCode',
            field=models.CharField(max_length=64, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='taskruntime',
            name='slaveCode',
            field=models.CharField(max_length=64, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='taskruntime',
            name='taskCode',
            field=models.CharField(max_length=64, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='template',
            name='content',
            field=models.TextField(null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='template',
            name='templateName',
            field=models.CharField(max_length=16, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='templateinstance',
            name='content',
            field=models.TextField(validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='templateinstance',
            name='instanceName',
            field=models.CharField(max_length=16, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='templateinstance',
            name='parameter',
            field=models.TextField(null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='templateinstance',
            name='templateCode',
            field=models.CharField(max_length=64, null=True, validators=[core.validator.validate_empty_str]),
        ),
        migrations.AlterField(
            model_name='templateinstance',
            name='userCode',
            field=models.CharField(max_length=64, null=True, validators=[core.validator.validate_empty_str]),
        ),
    ]