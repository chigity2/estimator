# Generated by Django 4.1.7 on 2023-03-30 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subnotes',
            name='employee',
            field=models.CharField(max_length=20),
        ),
    ]
