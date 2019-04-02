# Generated by Django 2.1.7 on 2019-04-02 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginRegister', '0004_auto_20190402_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='abcd', max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_seller',
            field=models.BooleanField(default=False, verbose_name='Seller'),
        ),
    ]
