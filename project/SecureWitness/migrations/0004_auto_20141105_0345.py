# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SecureWitness', '0003_auto_20141105_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, default=0, to='SecureWitness.User'),
            preserve_default=True,
        ),
    ]
