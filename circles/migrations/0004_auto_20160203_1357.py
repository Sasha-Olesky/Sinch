# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0003_topic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='circle',
            name='group',
            field=models.ForeignKey(to='circles.Group'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='circle',
            field=models.ForeignKey(related_name='topics', to='circles.Circle'),
        ),
    ]
