# Generated by Django 5.1.3 on 2024-11-14 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0005_alter_userchooseditem_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userchooseditem',
            old_name='chestplates',
            new_name='chestplate',
        ),
        migrations.RenameField(
            model_name='userchooseditem',
            old_name='helmets',
            new_name='helmet',
        ),
        migrations.RenameField(
            model_name='userchooseditem',
            old_name='leggings',
            new_name='legging',
        ),
    ]
