# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-21 11:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_customer"),
    ]

    operations = [
        migrations.DeleteModel(name="Cart",),
        migrations.DeleteModel(name="CartItem",),
        migrations.DeleteModel(name="Order",),
        migrations.DeleteModel(name="OrderItem",),
    ]
