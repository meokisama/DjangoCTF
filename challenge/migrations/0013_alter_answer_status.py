# Generated by Django 3.2.7 on 2022-12-24 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0012_answer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='status',
            field=models.CharField(max_length=10),
        ),
    ]
