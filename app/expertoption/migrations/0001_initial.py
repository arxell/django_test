# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-28 12:00
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('result_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('created_at', models.DateTimeField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('type', models.IntegerField(choices=[(1, 'deposit'), (2, 'withdrawal')], db_index=True, default=1)),
                ('created_at', models.DateTimeField(db_index=True)),
                ('trader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expertoption.Trader')),
            ],
        ),
        migrations.AddField(
            model_name='deal',
            name='trader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expertoption.Trader'),
        ),
    ]
