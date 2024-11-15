from django.contrib import admin
from .models import Helmet, Chestplate, Legging, Boots, UserInventory, UserChoosedItem, QuestNode, QuestEdge, NodeUser, UserLikes, SkillNode, SkillEdge, SkillUser

# Register your models here.
admin.site.register([Helmet, Chestplate, Legging, Boots, UserInventory, UserChoosedItem, QuestNode, QuestEdge, NodeUser, UserLikes, SkillNode, SkillEdge, SkillUser])