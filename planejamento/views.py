from django.shortcuts import render
from perfil.models import Categoria
from extrato.models import Valores
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json

def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias':categorias})

@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()
    return JsonResponse({'status': 'Success'})

def ver_planejamento(request):
    categorias = Categoria.objects.all()
    total_planejamento = 0
        
    for valor in categorias:
        total_planejamento += valor.valor_planejamento

    valores = Valores.objects.filter(data__month=datetime.now().month)
    total_valor_gasto = 0

    for valor in valores:
        total_valor_gasto += valor.valor

    def porcentagem_total_gasta():
        return int((total_valor_gasto * 100) / total_planejamento)

    return render(request, 'ver_planejamento.html', {'categorias': categorias, 'total_planejamento': total_planejamento, 'total_valor_gasto': total_valor_gasto, 'porcentagem_total_gasta':porcentagem_total_gasta})