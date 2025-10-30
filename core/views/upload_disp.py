from django.shortcuts import render, redirect
from core.models import Dispositivo 
from django.urls import reverse
from core.forms import DispositivoForm

def gerenciar_disp(request):
    if request.method == 'POST':
        form = DispositivoForm(request.POST)

        if form.is_valid():
            disp_instance = form.save(commit=False)

            disp_instance.save()
            #disp_instance.cadastrarDispositivoORM()

            if request.headers.get('Hx-request'):
                dispositivos = Dispositivo.objects.all().order_by('-idDispositivo')
                return render(request, 'core/partials/disp_list.html', {'dispositivos': dispositivos})
            
            return redirect(reverse('gerenciar_disp'))
        
        else:
            print(form.errors)


    else:
        form = DispositivoForm()
        dispositivos = Dispositivo.objects.all().order_by('-idDispositivo')
        return render(request, 'core/painel_dispositivo.html', {
            'dispositivos': dispositivos,
            'form': form,
            'form_errors': form.errors if request=='POST' else None,
        })
