# Generated by Django 3.0.8 on 2021-03-22 01:19

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210322_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='/author_pictures/default_pic_author.jpg', upload_to=users.models.profile_pic_path),
        ),
    ]
