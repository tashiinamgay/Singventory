# Generated by Django 4.1.3 on 2022-11-24 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SingventoryApp', '0016_alter_notification_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='svuser',
            name='category',
            field=models.CharField(choices=[('Admin', 'Admin'), ('User', 'User')], default='User', max_length=15, verbose_name='category'),
        ),
    ]