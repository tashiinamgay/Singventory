# Generated by Django 4.1.3 on 2022-11-22 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SingventoryApp', '0014_alter_borrow_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
