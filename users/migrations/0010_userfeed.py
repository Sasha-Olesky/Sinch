# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_post_count_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('circles', '0006_auto_20160205_1355'),
        ('users', '0009_userreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(default=b'Like', max_length=255, choices=[(b'Like', b'Like'), (b'Feedback', b'Feedback'), (b'PostComment', b'PostComment'), (b'TopicComment', b'TopicComment'), (b'Request', b'Request')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('action_user', models.ForeignKey(related_name='action_user', to=settings.AUTH_USER_MODEL)),
                ('like', models.ForeignKey(blank=True, to='posts.Like', null=True)),
                ('post_comment', models.ForeignKey(blank=True, to='posts.Comment', null=True)),
                ('topic_comment', models.ForeignKey(blank=True, to='circles.TopicComment', null=True)),
                ('user', models.ForeignKey(related_name='feed_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
