# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import SecureWitness.models


class Migration(migrations.Migration):

    dependencies = [
        ('SecureWitness', '0002_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepic',
            name='file',
            field=models.FileField(upload_to=SecureWitness.models.place_pic),
            preserve_default=True,
        ),
    ]
