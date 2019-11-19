# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20160523_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeed',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
