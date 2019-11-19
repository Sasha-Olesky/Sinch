# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='circle',
            name='group',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
