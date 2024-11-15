# Generated by Django 5.1.3 on 2024-11-14 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('item_type', models.CharField(choices=[('lether', 'lether'), ('chain_mail', 'chain_mail'), ('iron', 'iron'), ('gold', 'gold'), ('diamond', 'diamond'), ('netherite', 'netherite')], max_length=100)),
                ('skin', models.ImageField(upload_to='skins')),
                ('agreeableness', models.PositiveIntegerField(default=20)),
                ('emotional_stablility', models.PositiveIntegerField(default=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chestplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('item_type', models.CharField(choices=[('lether', 'lether'), ('chain_mail', 'chain_mail'), ('iron', 'iron'), ('gold', 'gold'), ('diamond', 'diamond'), ('netherite', 'netherite')], max_length=100)),
                ('skin', models.ImageField(upload_to='skins')),
                ('agreeableness', models.PositiveIntegerField(default=20)),
                ('emotional_stablility', models.PositiveIntegerField(default=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Helmet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('item_type', models.CharField(choices=[('lether', 'lether'), ('chain_mail', 'chain_mail'), ('iron', 'iron'), ('gold', 'gold'), ('diamond', 'diamond'), ('netherite', 'netherite')], max_length=100)),
                ('skin', models.ImageField(upload_to='skins')),
                ('agreeableness', models.PositiveIntegerField(default=20)),
                ('emotional_stablility', models.PositiveIntegerField(default=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Legging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('item_type', models.CharField(choices=[('lether', 'lether'), ('chain_mail', 'chain_mail'), ('iron', 'iron'), ('gold', 'gold'), ('diamond', 'diamond'), ('netherite', 'netherite')], max_length=100)),
                ('skin', models.ImageField(upload_to='skins')),
                ('agreeableness', models.PositiveIntegerField(default=20)),
                ('emotional_stablility', models.PositiveIntegerField(default=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boots', models.ManyToManyField(to='tinder.boots')),
                ('chestplates', models.ManyToManyField(to='tinder.chestplate')),
                ('helmets', models.ManyToManyField(to='tinder.helmet')),
                ('leggings', models.ManyToManyField(to='tinder.legging')),
            ],
        ),
    ]