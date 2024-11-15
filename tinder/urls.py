from django.urls import path
from .views import MainView, SignInView, RegisterView, pick_item, get_skill_graph_data, add_attr, remove_attr, get_quest_graph_data, get_cards, like_card, dislike_card

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('login/', SignInView.as_view(), name='signin'),
    path('register/', RegisterView.as_view(), name='signup'),
    
    path('api/pick_item/', pick_item, name='pick_item'),
    path('api/add_attr/<int:node_id>/', add_attr, name='add_attr'),
    path('api/remove_attr/', remove_attr, name='remove_attr'),
    path('api/quest-graph-data/', get_quest_graph_data, name='quest-graph-data'),
    path('api/skill-graph-data/', get_skill_graph_data, name='skill-graph-data'),
    path('api/get-cards/', get_cards, name='get-cards'),
    
    path('api/like-card/<int:liked_user_id>/', like_card, name="like-card"),
    path('api/dislike-card/<int:disliked_user_id>/', dislike_card, name='dislike-card'),
]
