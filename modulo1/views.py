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

def calculafp(request):
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
            break
        elif (ka * kxm) < 0:
            b = xm
        elif (ka * kxm) > 0:
            a = xm
        i += 1
    print('>>>>>>>>>>')
    return HttpResponse(json.dumps({ 'resultadofp': xm }), content_type="application/json")
    # render(request, 'modulo1/calculafp.html', {
    #     'resultadofp': xm,
    # })
