# Generated by Django 4.0.6 on 2022-07-27 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='rating_post',
            field=models.IntegerField(default=0),
        ),
    ]
