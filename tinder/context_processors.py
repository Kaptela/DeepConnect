from django.utils.timesince import timesince

def main(request):
    context = {
        # 'user_age' : timesince(request.user.date_of_birth),
        'pages' : {
            'header' : 'shared/header.html',
            'login' : 'page/login.html',
            'register' : 'page/register.html',
            'skilltree' : 'page/skilltree',
            'chat' : 'page/chat.html',
            'tinder' : 'page/tinder.html',
            'profile' : 'page/profile.html',
        }
    }
    
    return context