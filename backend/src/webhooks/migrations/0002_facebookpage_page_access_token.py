# Generated by Django 2.2.2 on 2019-06-04 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookpage',
            name='page_access_token',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
