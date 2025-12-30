from django.shortcuts import render

# Create your views here.
def show_settings(request):
    return render(request, 'core/show_settings.html', {'section_active': 'parametres'})


def show_stats(request):
    return render(request, 'core/show_stats.html', {'section_active':'statistiques'})