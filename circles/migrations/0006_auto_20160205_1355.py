# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0005_topiccomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='circle',
            name='permission',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='topiccomment',
            name='topic',
            field=models.ForeignKey(related_name='replies', to='circles.Topic'),
        ),
    ]
