# Generated by Django 4.1.3 on 2022-11-20 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SingventoryApp', '0004_borrow_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=15, verbose_name='status'),
        ),
    ]
