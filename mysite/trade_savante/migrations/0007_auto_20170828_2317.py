# Generated by Django 2.0.dev20170825085001 on 2017-08-28 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade_savante', '0006_auto_20170828_2316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tradeitem',
            old_name='file',
            new_name='image',
        ),
    ]
