# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20160314_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrate',
            name='message',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
