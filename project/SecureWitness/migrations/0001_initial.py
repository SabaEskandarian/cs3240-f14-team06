# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import SecureWitness.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField(default=datetime.date.today)),
                ('location', models.CharField(default=b'', max_length=100)),
                ('description', models.TextField(default=b'')),
                ('public', models.BooleanField(default=False)),
                ('author', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=SecureWitness.models.place_document)),
                ('user', models.CharField(max_length=100)),
                ('bulletin', models.ForeignKey(to='SecureWitness.Bulletin', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sharing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=100)),
                ('reader', models.CharField(max_length=100)),
                ('bulletin', models.ForeignKey(to='SecureWitness.Bulletin', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bulletin',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, default=0, to='SecureWitness.Folder'),
            preserve_default=True,
        ),
    ]
