# Generated by Django 3.2.7 on 2022-12-06 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='owner',
            field=models.CharField(default='chien', max_length=200),
            preserve_default=False,
        ),
    ]
