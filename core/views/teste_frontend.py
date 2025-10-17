from django.shortcuts import render
def teste_frontend(request):
    return render(request, 'core/testeView.html')
