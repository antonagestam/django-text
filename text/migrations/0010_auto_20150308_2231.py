# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0009_auto_20150304_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='type',
            field=models.CharField(default=b'markdown', max_length=20, choices=[(b'text', b'Text'), (b'markdown', b'Markdown'), (b'html', b'HTML')]),
            preserve_default=True,
        ),
    ]
