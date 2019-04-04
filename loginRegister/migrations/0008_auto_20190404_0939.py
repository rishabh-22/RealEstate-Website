# Generated by Django 2.1.7 on 2019-04-04 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginRegister', '0007_profile_phone_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_num',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='static/profile_pic.jpeg', upload_to='media/user_profilePics'),
        ),
    ]
