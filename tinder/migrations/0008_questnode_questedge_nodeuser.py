# Generated by Django 5.1.3 on 2024-11-14 22:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0007_rename_boots_userchooseditem_boot'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=1)),
                ('level', models.IntegerField()),
                ('label', models.CharField(max_length=20)),
                ('quest', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='QuestEdge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrows', models.CharField(default='to', editable=False, max_length=2)),
                ('from_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quest_node_from', to='tinder.questnode')),
                ('to_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quest_node_to', to='tinder.questnode')),
            ],
        ),
        migrations.CreateModel(
            name='NodeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tinder.questnode')),
            ],
        ),
    ]
