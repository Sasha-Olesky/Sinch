# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(default=b'/media/default_images/default.png', upload_to=utils.get_file_path),
        ),
    ]
