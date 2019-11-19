# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151122_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(default=b'/static/default_images/default.png', upload_to=users.models.get_file_path),
        ),
    ]
