# Generated by Django 2.0.dev20170825085001 on 2017-09-06 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trade_savante', '0011_tradesequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradesequence',
            name='sequencer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]