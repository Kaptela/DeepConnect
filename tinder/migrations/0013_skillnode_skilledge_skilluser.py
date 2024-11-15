# Generated by Django 5.1.3 on 2024-11-15 03:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0012_alter_userlikes_dislikes_alter_userlikes_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=1)),
                ('level', models.IntegerField()),
                ('label', models.CharField(max_length=20)),
                ('agreeableness', models.PositiveIntegerField()),
                ('emotional_stablility', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SkillEdge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrows', models.CharField(default='to', editable=False, max_length=2)),
                ('from_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_node_from', to='tinder.skillnode')),
                ('to_node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skill_node_to', to='tinder.skillnode')),
            ],
        ),
        migrations.CreateModel(
            name='SkillUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.BooleanField(default=False)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tinder.skillnode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
