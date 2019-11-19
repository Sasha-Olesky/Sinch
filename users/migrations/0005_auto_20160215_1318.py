# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20151123_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_facebook',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_instagram',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_twitter',
            field=models.BooleanField(default=False),
        ),
    ]
