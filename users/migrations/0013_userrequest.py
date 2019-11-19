# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0012_auto_20160402_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allow', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('request_user', models.ForeignKey(related_name='request_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
