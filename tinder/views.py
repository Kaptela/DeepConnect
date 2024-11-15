import json
from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.forms import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.core import serializers
from django.db.models import Q
from datetime import datetime
from django.utils.timesince import timesince
from django.contrib.auth import logout

from .forms import LoginForm, SignUpForm
from .models import UserInventory, UserChoosedItem, Helmet, Chestplate, Legging, Boots, QuestNode, QuestEdge, UserLikes, NodeUser, SkillNode, SkillEdge, SkillUser
from user.models import User

# Create your views here.
class MainView(TemplateView):
    template_name = 'pages/main.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_authenticated:
            
            user_likes, d = UserLikes.objects.get_or_create(user=user)
            liked_users = user_likes.likes.all()
            print('user_likes: ', user_likes)

            mutual_likes = []
            for liked_user in liked_users:
                liked_user_likes, c = UserLikes.objects.get_or_create(user=liked_user)
                if user in liked_user_likes.likes.all():
                    mutual_likes.append(liked_user)
            
            if mutual_likes:
                second_node = get_object_or_404(QuestNode, id=2)
                second_quest, quest_created = NodeUser.objects.get_or_create(user=user, node=second_node)
                
                # Set quest as done and save
                second_quest.is_done = True
                second_quest.save()
            
            context.update(
                user_invontory = UserInventory.objects.filter(user=user).first(),
                user_choosed_items = UserChoosedItem.objects.filter(user=user).first(),
                user_likes = mutual_likes,
                user_age = timesince(user.date_of_birth, datetime.now())
            )
            
            if context['user_choosed_items']:
                user.agreeableness += getattr(context['user_choosed_items'].helmet, 'agreeableness', 0)
                user.agreeableness += getattr(context['user_choosed_items'].chestplate, 'agreeableness', 0)
                user.agreeableness += getattr(context['user_choosed_items'].legging, 'agreeableness', 0)
                user.agreeableness += getattr(context['user_choosed_items'].boot, 'agreeableness', 0)
                
                user.emotional_stablility += getattr(context['user_choosed_items'].helmet, 'emotional_stablility', 0)
                user.emotional_stablility += getattr(context['user_choosed_items'].chestplate, 'emotional_stablility', 0)
                user.emotional_stablility += getattr(context['user_choosed_items'].legging, 'emotional_stablility', 0)
                user.emotional_stablility += getattr(context['user_choosed_items'].boot, 'emotional_stablility', 0)
            return context
            
    
class SignInView(LoginView):
    template_name = 'pages/main.html'
    redirect_authenticated_user = True
    form_class = LoginForm
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context.update(
            LoginForm = self.form_class
        )
        
        return context
    
class RegisterView(CreateView):
    form_class = SignUpForm
    template_name = 'pages/main.html'
    success_url = reverse_lazy('main')

    def get_success_url(self) -> str:
        success_url = super().get_success_url()
        success_url += f'?isFormValid={True}'
        return success_url

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        self.isFormValid = False
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            SignUpForm = self.form_class
        )
        return context

def custom_logout_view(request):
    logout(request)
    return redirect('/')
    
@csrf_exempt
@require_POST
def pick_item(request):
    data = json.loads(request.body)
    item_type = data.get('item_type')
    item_id = data.get('item_id')
    
    items = {
        'helmet' : Helmet,
        'chestplate' : Chestplate,
        'legging' : Legging,
        'boot' : Boots
    }

    if not item_type or not item_id:
        return JsonResponse({'success': 'False', 'error': 'Missing item_type or item_id'}, status=400)

    valid_item_types = ['helmet', 'chestplate', 'legging', 'boot']
    if item_type not in valid_item_types:
        return JsonResponse({'success': 'False', 'error': 'Invalid item_type'}, status=400)

    try:
        user_choosed_item = get_object_or_404(UserChoosedItem, user=request.user)
        
        item = get_object_or_404(items[item_type], id=item_id)
            
        print(user_choosed_item.helmet)
        setattr(user_choosed_item, item_type, item)  # Dynamically set the field
        user_choosed_item.save()
        return JsonResponse({'success': 'True', 'skin' : item.skin.url})
    except Exception as e:
        return JsonResponse({'success': 'False', 'error': str(e)}, status=500)
        
        
@csrf_exempt
@require_POST
def add_attr(request, node_id):
    try:
        user = request.user
        node = get_object_or_404(SkillNode, id=node_id)
        
        skill_user, c = SkillUser.objects.get_or_create(user=user, node = node, is_done=True)
        
        

        setattr(user, 'agreeableness', user.agreeableness + node.agreeableness)
        setattr(user, 'emotional_stablility', user.emotional_stablility + node.emotional_stablility)
        user.save()
        return JsonResponse({'success': 'True'}, status=200)
    except Exception as e:
        return JsonResponse({'success': 'False', 'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def remove_attr(request):
    data = json.loads(request.body)
    agreeableness = data.get('agreeableness')
    emotional_stablility = data.get('emotional_stablility')
    
    if not agreeableness or not emotional_stablility:
        return JsonResponse({'success': 'False', 'error': 'Missing agreeableness or emotional_stablility'}, status=400)
    
    try:
        user = request.user

        setattr(user, 'agreeableness', user.agreeableness - int(agreeableness.split('-')[1]))
        setattr(user, 'emotional_stablility', user.emotional_stablility - int(emotional_stablility.split('-')[1]))
        user.save()
        return JsonResponse({'success': 'True'})
    except Exception as e:
        return JsonResponse({'success': 'False', 'error': str(e)}, status=500)
    
    
def get_quest_graph_data(request):
    # Fetch nodes from the database
    nodes = list(QuestNode.objects.values('id', 'value', 'level', 'label', 'quest'))
    completed_nodes = NodeUser.objects.filter(user=request.user).values_list('node', flat=True)
    # print(completed_nodes)
    # Modify labels to include value (similar to the .map function in JavaScript)
    for node in nodes:
        if node['id'] in completed_nodes:
            node['selected'] = True
        node['label'] += f" \n({node['value']})"

    # Fetch edges from the database
    edges = list(QuestEdge.objects.values('from_node', 'to_node', 'arrows'))
    # Rename fields to match the JavaScript format
    edges = [{'from': edge['from_node'], 'to': edge['to_node'], 'arrows': edge['arrows']} for edge in edges]

    # Return the data as JSON
    return JsonResponse({'nodes': nodes, 'edges': edges})

def get_skill_graph_data(request):
    nodes = list(SkillNode.objects. values('id', 'value', 'level', 'label', 'agreeableness', 'emotional_stablility'))
    completed_nodes = SkillUser.objects.filter(user=request.user).values_list('node', flat=True)
    
    for node in nodes:
        if node['id'] in completed_nodes:
            node['selected'] = True
        else:
            node['selected'] = False
        node['label'] += f'\n({node['value']})'
    
    edges = list(SkillEdge.objects.values('from_node', 'to_node', 'arrows'))
    
    edges = [{'from': edge['from_node'], 'to': edge['to_node'], 'arrows': edge['arrows']} for edge in edges]
    
    return JsonResponse({'nodes': nodes, 'edges': edges})
    
    
def get_cards(request):
    user = request.user
    
    # Validate user attributes
    try:
        agreeableness_min = int(user.agreeableness) - 10
        agreeableness_max = int(user.agreeableness) + 10
        
        emotional_stability_min = int(user.emotional_stablility) - 10
        emotional_stability_max = int(user.emotional_stablility) + 10
    except AttributeError as e:
        raise ValueError("User object does not have the required attributes") from e

    # Query the database
    try:
        likes_dislikes, c = UserLikes.objects.get_or_create(user=user)
        cards = User.objects.filter(
            ~Q(sex=user.sex),
            agreeableness__gte=agreeableness_min,
            agreeableness__lte=agreeableness_max,
            emotional_stablility__gte=emotional_stability_min,
            emotional_stablility__lte=emotional_stability_max,
        ).exclude(
            Q(id__in=likes_dislikes.likes.values_list('id', flat=True)) | 
            Q(id__in=likes_dislikes.dislikes.values_list('id', flat=True))    
        ).exclude(id=user.id)
        

        return JsonResponse({'card':  serializers.serialize('json', cards)})
    except Exception as e:
        raise ValueError("Error occurred while querying the database", e) from e
    
@csrf_exempt
@require_POST
def like_card(request, liked_user_id):
    try:
        user = request.user
        
        # Get or create the user likes object
        user_likes, created = UserLikes.objects.get_or_create(user=user)
        
        # Get the liked user object, ensuring it exists
        liked_user = get_object_or_404(User, id=liked_user_id)
        
        # Add liked_user only if not already liked
        if not user_likes.likes.filter(id=liked_user.id).exists():
            user_likes.likes.add(liked_user)
        
        # Check if UserLikes was just created to initialize first quest
        if user_likes.likes.count() == 1:
            first_node = get_object_or_404(QuestNode, id=1)
            first_quest, quest_created = NodeUser.objects.get_or_create(user=user, node=first_node)
            
            # Set quest as done and save
            first_quest.is_done = True
            first_quest.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        # Convert exception to string for JSON response
        return JsonResponse({"success": False, "error": str(e)})
    
    
    
    
@csrf_exempt
@require_POST
def dislike_card(request, disliked_user_id):
    try:
        user = request.user
        
        user_likes, c = UserLikes.objects.get_or_create(user=user)
        disliked_user = get_object_or_404(User, id=disliked_user_id)
        
        user_likes.dislikes.add(disliked_user)
        
        return JsonResponse({'success' : True})
    except Exception as e:
        return JsonResponse({"success" : False, "error" : e})