# Generated by Django 3.2 on 2021-07-30 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locationapp', '0002_auto_20210728_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='coordinates',
            field=models.CharField(blank=True, max_length=40, verbose_name='координаты'),
        ),
    ]