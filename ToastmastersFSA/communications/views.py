from django.shortcuts import render

# Create your views here.
def manage_communications(request):
    return render(request, "communications/show_communications.html")