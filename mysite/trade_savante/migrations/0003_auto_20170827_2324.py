# Generated by Django 2.0.dev20170825085001 on 2017-08-27 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_savante', '0002_auto_20170827_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(choices=[('bi', 'Bike'), ('ls', 'Leisure'), ('sp', 'Sports'), ('fn', 'Fashion'), ('bk', 'Books'), ('na', 'Not Applicable')], default='na', max_length=2),
        ),
    ]
