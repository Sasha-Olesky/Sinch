# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_userfeed_user_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfeed',
            name='user_rate',
            field=models.ForeignKey(blank=True, to='users.UserRate', null=True),
        ),
    ]
