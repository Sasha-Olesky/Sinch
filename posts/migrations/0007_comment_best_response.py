# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_commentlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='best_response',
            field=models.BooleanField(default=False),
        ),
    ]
