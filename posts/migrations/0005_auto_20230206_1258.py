# Generated by Django 2.2.9 on 2023-02-06 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20230206_1255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='groups',
            new_name='group',
        ),
    ]
