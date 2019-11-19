# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comment_count',
        ),
        migrations.RemoveField(
            model_name='post',
            name='like_count',
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='post_comments', to='posts.Post'),
        ),
    ]
