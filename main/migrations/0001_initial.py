# Generated by Django 4.1.2 on 2022-10-24 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
