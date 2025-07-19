from django.shortcuts import render,redirect
from .models import Citation, Like
from .forms import CitationForm
import numpy as np
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count


def index(request):
    cit_ids = np.array(Citation.objects.values_list('id', flat=True))
    cit_weight_int = np.array(Citation.objects.values_list('weight', flat=True))
    cit_weight_float = cit_weight_int.astype(float)
    cit_weight_float = cit_weight_float/np.sum(cit_weight_float)
    element = np.random.choice(cit_ids, p=cit_weight_float)
    select_cit = Citation.objects.get(id=element)
    is_liked = False
    session_key = f'post_{select_cit.id}_viewed'


    if request.user.is_authenticated:
        is_liked = Like.objects.filter(cit=select_cit, user=request.user).exists()
    elif not request.session.session_key:
        is_liked = Like.objects.filter(cit=select_cit, session_id=request.session.session_key).exists()

    if not request.session.get(session_key, False):
        select_cit.views += 1
        select_cit.save()
        # Помечаем как просмотренный
        request.session[session_key] = True
        # Устанавливаем время жизни сессии
        request.session.set_expiry(60 * 60 * 24)  # 24 часа

    return render(request, 'main/index.html',{
        'cit': select_cit,
        'is_liked': is_liked,
        'total_likes': select_cit.total_likes
    })
    #return render(request, 'main/index.html', { 'cit': cit })

def handle_like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        select_cit = get_object_or_404(Citation, id=post_id)

        # Если у сессии нет ключа - создаем его
        if not request.session.session_key:
            request.session.create()  # Создаем новую сессию

        # Проверяем, есть ли уже лайк от этого пользователя/сессии
        if request.user.is_authenticated:
            # Для авторизованных пользователей проверяем по user
            like_exists = Like.objects.filter(cit=select_cit, user=request.user).exists()
        else:
            # Для анонимных - по session_id
            like_exists = Like.objects.filter(cit=select_cit, session_id=request.session.session_key).exists()

        # Обрабатываем лайк/анлайк
        if like_exists:
            # Если лайк уже есть - удаляем его (анлайк)
            if request.user.is_authenticated:
                Like.objects.filter(cit=select_cit, user=request.user).delete()
            else:
                Like.objects.filter(cit=select_cit, session_id=request.session.session_key).delete()
            liked = False  # Статус после действия
        else:
            # Если лайка нет - создаем новый
            Like.objects.create(
                cit=select_cit,
                user=request.user if request.user.is_authenticated else None,
                session_id=request.session.session_key if not request.user.is_authenticated else None
            )
            liked = True  # Статус после действия
        return JsonResponse({
            'is_liked': liked,
            'total_likes': select_cit.likes.count()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def newc(request):
    error = ''
    if request.method == "POST":
        form = CitationForm(request.POST)
        if form.is_valid():
            new_cit = Citation.objects.filter(film=form.instance.film)
            count_film = new_cit.count()
            if count_film>=3:
                error = '!!!  Уже существует 3 цитаты по этому произведению'
            else:
                dd = True
                for single_cit in new_cit:
                    if single_cit.title == form.instance.title:
                        dd = False
                        break
                    else:
                        dd = True
                if dd:
                    form.save()
                    return redirect('home')
                else:
                    error = '!!!  Такая цитата уже есть в базе данных'
        else:
            error = '!!!  Форма была неверной'

    form = CitationForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/newc.html', context)


def topc(request):
    count_cit = Citation.objects.count()
    if count_cit >=10:
        count_cit = 10
    #cit = Citation.objects.order_by('-id')[:count_cit]
    cit = Citation.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')[:count_cit]
    return render(request, 'main/topc.html', {'tasks': cit })