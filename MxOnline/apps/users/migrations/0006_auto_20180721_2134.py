# Generated by Django 2.0.6 on 2018-07-21 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180721_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码'), ('update_email', '修改密码')], max_length=10, verbose_name='验证码类型'),
        ),
    ]
