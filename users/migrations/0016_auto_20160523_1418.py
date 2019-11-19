# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0015_auto_20160505_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfinityBan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_unique_id', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='device_unique_id',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
