from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def teste_frontend(request):
    return render(request, 'teste_frontend.html')

