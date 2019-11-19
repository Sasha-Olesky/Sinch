# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import circles.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_userfeed'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeed',
            name='user_rate',
            field=models.ForeignKey(blank=circles.models.TopicComment, to='users.UserRate', null=True),
        ),
    ]
