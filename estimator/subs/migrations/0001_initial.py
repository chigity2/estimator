# Generated by Django 4.1.7 on 2023-03-29 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Subcontractors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address1', models.CharField(max_length=50)),
                ('address2', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=12)),
                ('phone', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Trades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=12)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SubTrades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subs.subcontractors')),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subs.trades')),
            ],
        ),
        migrations.CreateModel(
            name='SubNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subs.employees')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subs.subcontractors')),
            ],
        ),
        migrations.CreateModel(
            name='PrimaryContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subs.employees')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subs.subcontractors')),
            ],
        ),
        migrations.AddField(
            model_name='employees',
            name='sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subs.subcontractors'),
        ),
    ]
