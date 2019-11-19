# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20160205_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='count_likes',
            field=models.IntegerField(default=0),
        ),
    ]
