# Generated by Django 4.1.3 on 2022-11-21 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SingventoryApp', '0006_alter_borrow_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Return', 'Return'), ('Returned', 'Returned')], default='Pending', max_length=15, verbose_name='status'),
        ),
    ]
