# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_comment_best_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='permission',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='permission',
            field=models.BooleanField(default=True),
        ),
    ]
