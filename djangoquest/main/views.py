from django.shortcuts import render,redirect
from .models import Citation
from .forms import CitationForm
import numpy as np


def index(request):
    cit_ids = np.array(Citation.objects.values_list('id', flat=True))
    cit_weight_int = np.array(Citation.objects.values_list('weight', flat=True))
    cit_weight_float = cit_weight_int.astype(float)
    cit_weight_float = cit_weight_float/np.sum(cit_weight_float)
    element = np.random.choice(cit_ids, p=cit_weight_float)
    cit = Citation.objects.get(id=element)

    return render(request, 'main/index.html', { 'cit': cit })

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
                dd = False
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
    count = Citation.objects.count()
    if count >=10:
        count = 10
    cit = Citation.objects.order_by('-likes')[:count]
    return render(request, 'main/topc.html', {'tasks': cit })