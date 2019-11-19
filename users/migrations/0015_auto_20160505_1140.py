# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_userfeed_user_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='facebook_url',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='instagram_url',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitter_url',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
