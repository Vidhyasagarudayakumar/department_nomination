# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-02 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('da', '0004_auto_20170302_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='reference3',
            field=models.CharField(max_length=25, null=True),
        ),
    ]