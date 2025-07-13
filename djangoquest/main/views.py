from django.shortcuts import render,redirect
from .models import Citation
from .forms import CitationForm
import random


def index(request):

    cit = Citation.objects.all()
    #return render(request, 'main/index.html', {'title': 'Главная страница', 'tasks': cit})
    return render(request, 'main/index.html', { 'tasks': cit })

def newc(request):
    error = ''
    if request.method == "POST":
        form = CitationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'
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