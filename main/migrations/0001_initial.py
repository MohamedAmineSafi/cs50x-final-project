# Generated by Django 4.1.9 on 2023-05-30 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('birthday', models.CharField(max_length=128)),
                ('hobbies', models.CharField(max_length=255)),
                ('personality', models.CharField(max_length=255)),
            ],
        ),
    ]
