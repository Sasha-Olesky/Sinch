# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('circles', '0004_auto_20160203_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('permission', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(to='circles.Topic')),
            ],
        ),
    ]
