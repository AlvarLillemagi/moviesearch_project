# Generated by Django 5.1 on 2024-08-24 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviesearch', '0002_remove_bookmark_overview_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmdb_id', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('overview', models.TextField()),
                ('release_date', models.CharField(max_length=10)),
                ('poster_path', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
