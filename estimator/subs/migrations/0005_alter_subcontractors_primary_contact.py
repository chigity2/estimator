# Generated by Django 4.1.7 on 2023-03-30 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0004_alter_subcontractors_primary_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcontractors',
            name='primary_contact',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
