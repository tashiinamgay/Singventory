# Generated by Django 4.1.3 on 2022-11-20 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SingventoryApp', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='svuser',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]
