from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
import numpy as np
import scipy as sp
import json
from django.http import HttpResponse
# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'modulo1/index.html'

class FalsaPosicaoView(generic.TemplateView):
    template_name = 'modulo1/falsaposicao.html'

class SecanteView(generic.TemplateView):
    template_name = 'modulo1/secante.html'

class MullerView(generic.TemplateView):
    template_name = 'modulo1/muller.html'

def calculafp(request):
    pontos = []
    a = int(request.POST.get('xl'))
    b = int(request.POST.get('xu'))
    f = lambda x: eval(request.POST.get('f'))
    maxi = int(request.POST.get('maxi'))
    tol = float(request.POST.get('tol'))
    ka = f(a)
    kb = f(b)
    i = 0
    while i < maxi:
        xm = (b * ka - a * kb) / (ka - kb)
        kxm = f(xm)
        if abs(a - b) < tol:
            pontos.append([xm, kxm])
            break
        elif (ka * kxm) < 0:
            b = xm
            pontos.append([xm, kxm])
        elif (ka * kxm) > 0:
            a = xm
            pontos.append([xm, kxm])
        i += 1
    return HttpResponse(json.dumps({ 'points': pontos }), content_type="application/json")