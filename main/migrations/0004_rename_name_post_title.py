# Generated by Django 4.1.2 on 2022-11-02 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_room_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='name',
            new_name='title',
        ),
    ]