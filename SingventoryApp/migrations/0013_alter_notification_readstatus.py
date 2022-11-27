# Generated by Django 4.1.3 on 2022-11-22 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SingventoryApp', '0012_alter_notification_readstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='readStatus',
            field=models.CharField(choices=[('unread', 'unread'), ('read', 'read')], default='unread', max_length=15, verbose_name='readStatus'),
        ),
    ]