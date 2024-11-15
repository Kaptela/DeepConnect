from django.db import models

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=50)
    
    ITEM_TYPE_CHOICES = {
        'lether' : 'lether',
        'chain_mail' : 'chain_mail',
        'iron' : 'iron',
        'gold' : 'gold',
        'diamond' : 'diamond', 
        'netherite' : 'netherite',
    }
    item_type = models.CharField(choices=ITEM_TYPE_CHOICES, max_length=100)
    
    # ITEM_SLOT_CHOICES = {
    #     'helmet' : 'helmet',
    #     'Chestplate' : 'Chestplate',
    #     'Leggings' : 'Leggings',
    #     'boots' : 'boots',
    # }
    # item_slot = models.CharField(choices=ITEM_SLOT_CHOICES, max_length=100)
    
    skin = models.ImageField(upload_to='skins')
    
    agreeableness = models.PositiveIntegerField(default=20)
    emotional_stablility = models.PositiveIntegerField(default=20)
    
    
    def __str__(self):
        return f'{self.item_name}'

    class Meta:
        abstract = True
        
class Helmet(Item):
    ...
    
class Chestplate(Item):
    ...
    
class Legging(Item):
    ...
    
class Boots(Item):
    ...
    
class UserInventory(models.Model):
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE, unique=True)
    helmets = models.ManyToManyField(to='tinder.Helmet', blank=True, null=True)
    chestplates = models.ManyToManyField(to='tinder.Chestplate', blank=True, null=True)
    leggings = models.ManyToManyField(to='tinder.Legging', blank=True, null=True)
    boots = models.ManyToManyField(to='tinder.Boots', blank=True, null=True)
    
    def __str__(self):
        return f'Inventory of {self.user}'
    
class UserChoosedItem(models.Model):
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE, unique=True)
    helmet = models.ForeignKey(to='tinder.Helmet', on_delete=models.CASCADE, blank=True, null=True)
    chestplate = models.ForeignKey(to='tinder.Chestplate', on_delete=models.CASCADE, blank=True, null=True)
    legging = models.ForeignKey(to='tinder.Legging', on_delete=models.CASCADE, blank=True, null=True)
    boot = models.ForeignKey(to='tinder.Boots', on_delete=models.CASCADE, blank=True, null=True)
    
    
class QuestNode(models.Model):
    value = models.IntegerField(default=1)
    level = models.IntegerField()
    label = models.CharField(max_length=20)
    quest = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.id} {self.quest}'
    
    
class QuestEdge(models.Model):
    from_node = models.ForeignKey(to='tinder.QuestNode', on_delete=models.CASCADE, related_name='quest_node_from')
    to_node = models.ForeignKey(to='tinder.QuestNode', on_delete=models.CASCADE, related_name='quest_node_to', blank=True, null=True)
    arrows = models.CharField(editable=False, default='to', max_length=2)
    
    def __str__(self):
        return f'{self.from_node} -> {self.to_node}'
    
class NodeUser(models.Model):
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE)
    node = models.ForeignKey(to='tinder.QuestNode', on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    
    
    

class SkillNode(models.Model):
    value = models.IntegerField(default=1)
    level = models.IntegerField()
    label = models.CharField(max_length=20)
    agreeableness = models.PositiveIntegerField()
    emotional_stablility = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.label} - {self.level} {self.agreeableness}:{self.emotional_stablility}'
    
class SkillEdge(models.Model):
    from_node = models.ForeignKey(to='tinder.SkillNode', on_delete=models.CASCADE, related_name='skill_node_from')
    to_node = models.ForeignKey(to='tinder.SkillNode', on_delete=models.CASCADE, related_name='skill_node_to', blank=True, null=True)
    arrows = models.CharField(editable=False, default='to', max_length=2)
    
    def __str__(self):
        return f'{self.from_node} -> {self.to_node}'
    
class SkillUser(models.Model):
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE)
    node = models.ForeignKey(to='tinder.SkillNode', on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)


class UserLikes(models.Model):
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE, unique=True)
    likes = models.ManyToManyField(to='user.User', related_name='likes', blank=True)
    dislikes = models.ManyToManyField(to='user.User', related_name='dislike', blank=True)
    
    def __str__(self):
        return f'likes of {self.user}'