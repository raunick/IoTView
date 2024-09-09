from django.shortcuts import render

def gerar_relatorio(request):
    # Lógica para gerar relatórios será implementada aqui
    return render(request, 'relatorio/gerar_relatorio.html')
