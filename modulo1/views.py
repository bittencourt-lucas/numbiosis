from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
import numpy as np
import scipy as sp

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'modulo1/index.html'

class FalsaPosicaoView(generic.TemplateView):
    template_name = 'modulo1/falsaposicao.html'

def calculafp(request):
    a = int(request.POST['xl'])
    b = int(request.POST['xu'])
    f = lambda x: eval(request.POST['f'])
    maxi = int(request.POST['maxi'])
    tol = float(request.POST['tol'])
    ka = f(a)
    print(ka)
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
    return render(request, 'modulo1/calculafp.html', {
        'resultadofp': xm,
    })
