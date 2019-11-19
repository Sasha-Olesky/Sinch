# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_auto_20160223_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.IntegerField(default=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(related_name='receiver_rate', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='sender_rate', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='count_rates',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
