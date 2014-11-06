# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SecureWitness', '0002_auto_20141104_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, default=0, to='SecureWitness.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, default=0, to='SecureWitness.Folder'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='bulletin',
            field=models.ForeignKey(to='SecureWitness.Bulletin', on_delete=django.db.models.deletion.DO_NOTHING),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='folder',
            name='user',
            field=models.ForeignKey(to='SecureWitness.User', on_delete=django.db.models.deletion.DO_NOTHING),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sharing',
            name='author',
            field=models.ForeignKey(related_name='sharing_author', on_delete=django.db.models.deletion.DO_NOTHING, to='SecureWitness.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sharing',
            name='bulletin',
            field=models.ForeignKey(to='SecureWitness.Bulletin', on_delete=django.db.models.deletion.DO_NOTHING),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sharing',
            name='reader',
            field=models.ForeignKey(related_name='sharing_reader', on_delete=django.db.models.deletion.DO_NOTHING, to='SecureWitness.User'),
            preserve_default=True,
        ),
    ]
