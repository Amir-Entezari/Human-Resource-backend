# Generated by Django 4.2.2 on 2023-07-01 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timetrack',
            old_name='entry_time',
            new_name='checkout_time',
        ),
        migrations.RemoveField(
            model_name='timetrack',
            name='exit_time',
        ),
        migrations.AddField(
            model_name='timetrack',
            name='checkout_type',
            field=models.CharField(choices=[('E', 'Enter'), ('Q', 'Quit')], default='E', max_length=1),
        ),
    ]
