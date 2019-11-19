# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0008_userrate_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('reported', models.ForeignKey(related_name='reported_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='who_report_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
