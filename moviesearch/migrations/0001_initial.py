# Generated by Django 5.1 on 2024-08-23 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('release_date', models.CharField(max_length=10)),
                ('overview', models.TextField()),
            ],
        ),
    ]
