# Generated by Django 2.0.6 on 2018-07-21 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180708_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='image/default.png', null=True, upload_to='image/%Y/%m', verbose_name='头像'),
        ),
    ]
