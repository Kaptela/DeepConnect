# Generated by Django 5.1.3 on 2024-11-14 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='ava'),
        ),
    ]