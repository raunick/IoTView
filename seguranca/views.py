from django.shortcuts import render

def gerenciar_seguranca(request):
    # Lógica de segurança será implementada aqui
    return render(request, 'seguranca/gerenciar_seguranca.html')
