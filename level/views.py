from django.shortcuts import render
from .models import Level

# Create your views here.

def index(request):
    return render(request, 'index.html')

def level_mainlist(request):
    main_levels = Level.objects.filter(ranking__lte=75)
    return render(request, 'level_mainlist.html', {'main_levels': main_levels})

def level_extendedlist(request):
    extended_levels = Level.objects.filter(ranking__range=(76, 150))
    return render(request, 'level_extendedlist.html', {'extended_levels': extended_levels})

def level_legacylist(request):
    legacy_levels = Level.objects.filter(ranking__gt=150)
    return render(request, 'level_legacylist.html', {'legacy_levels': legacy_levels})

def level_detail(request, level_id):
    level = Level.objects.get(pk=level_id)
    return render(request, 'level_detail.html', {'level': level})

def is_admin(user):
    return user.is_superuser