# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('SecureWitness', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='author',
            field=models.ForeignKey(default=0, to='SecureWitness.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='date',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='description',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='folder',
            field=models.ForeignKey(default=0, to='SecureWitness.Folder'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='location',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
    ]
