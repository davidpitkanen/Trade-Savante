# Generated by Django 2.0.dev20170825085001 on 2017-09-17 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_savante', '0017_remove_tradeitem_key_words'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchkeywords',
            name='wordsearch',
        ),
        migrations.AddField(
            model_name='searchkeywords',
            name='key_word',
            field=models.TextField(null=True),
        ),
    ]