# Generated by Django 3.2.16 on 2022-10-27 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='customer_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
