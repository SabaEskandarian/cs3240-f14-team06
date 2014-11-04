# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('public', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'')),
                ('bulletin', models.ForeignKey(to='SecureWitness.Bulletin')),
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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sharing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('passHash', models.CharField(max_length=200)),
                ('isAdmin', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sharing',
            name='author',
            field=models.ForeignKey(related_name='sharing_author', to='SecureWitness.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sharing',
            name='bulletin',
            field=models.ForeignKey(to='SecureWitness.Bulletin'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sharing',
            name='reader',
            field=models.ForeignKey(related_name='sharing_reader', to='SecureWitness.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='folder',
            name='user',
            field=models.ForeignKey(to='SecureWitness.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bulletin',
            name='author',
            field=models.ForeignKey(to='SecureWitness.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bulletin',
            name='folder',
            field=models.ForeignKey(to='SecureWitness.Folder'),
            preserve_default=True,
        ),
    ]
