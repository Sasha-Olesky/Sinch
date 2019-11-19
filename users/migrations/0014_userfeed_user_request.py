# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_userrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeed',
            name='user_request',
            field=models.ForeignKey(blank=True, to='users.UserRequest', null=True),
        ),
    ]
